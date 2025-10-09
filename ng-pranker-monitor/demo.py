import asyncio
import glob
import json
import math
import os
import random
import time
from typing import Set

import aiohttp_cors
import websockets
from aiohttp import web


class MetricProducer:
    def __init__(self):
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.running = False
        self.stats = {
            "messages_sent": 0,
            "messages_failed": 0,
            "client_count": 0,
            "last_send_time": 0,
            "send_delays": [],
        }
        self.frame_files = []
        self.current_frame_index = 0
        self.load_frame_files()

    def load_frame_files(self):
        """Load all frame files from test-data directory"""
        test_data_dir = "test-data"
        if os.path.exists(test_data_dir):
            # Find all left_frame.jpg files
            pattern = os.path.join(test_data_dir, "at=*/left_frame.jpg")
            self.frame_files = sorted(glob.glob(pattern))
            print(f"Loaded {len(self.frame_files)} frame files")
        else:
            print("test-data directory not found")

    async def register_client(self, websocket):
        self.clients.add(websocket)
        self.stats["client_count"] = len(self.clients)
        print(f"Client connected. Total clients: {len(self.clients)}")

    async def unregister_client(self, websocket):
        self.clients.discard(websocket)
        self.stats["client_count"] = len(self.clients)
        print(f"Client disconnected. Total clients: {len(self.clients)}")

    async def broadcast_metric(self, data):
        if self.clients:
            start_time = time.time()
            message = json.dumps(data)

            # Track send delays for backpressure monitoring
            if self.stats["last_send_time"] > 0:
                delay = start_time - self.stats["last_send_time"]
                self.stats["send_delays"].append(delay)
                # Keep only last 100 delays
                if len(self.stats["send_delays"]) > 100:
                    self.stats["send_delays"].pop(0)

            self.stats["last_send_time"] = start_time

            try:
                results = await asyncio.gather(
                    *[client.send(message) for client in self.clients],
                    return_exceptions=True,
                )

                # Count successes and failures
                success_count = sum(
                    1 for result in results if not isinstance(result, Exception)
                )
                fail_count = len(results) - success_count

                self.stats["messages_sent"] += success_count
                self.stats["messages_failed"] += fail_count

                # Log backpressure warnings
                if fail_count > 0:
                    print(
                        f"Warning: {fail_count} messages failed to send (potential backpressure)"
                    )

            except Exception as e:
                self.stats["messages_failed"] += len(self.clients)
                print(f"Broadcast error: {e}")

    async def generate_noisy_sine_wave(self):
        """Generate noisy sine wave data"""
        t = 0
        while self.running:
            # Generate sine wave with noise
            sine_value = math.sin(t) * 10  # Amplitude of 10
            noise = random.uniform(-0.3, 0.3)  # Random noise between -2 and 2
            value = sine_value + noise

            # Calculate backpressure metrics
            avg_delay = (
                sum(self.stats["send_delays"]) / len(self.stats["send_delays"])
                if self.stats["send_delays"]
                else 0
            )
            failure_rate = (
                self.stats["messages_failed"]
                / (self.stats["messages_sent"] + self.stats["messages_failed"])
                if (self.stats["messages_sent"] + self.stats["messages_failed"]) > 0
                else 0
            )

            # Create metric data
            metric_data = {
                "name": "noisy_sine_wave",
                "val": round(value, 2),
                "timestamp": int(time.time() * 1000),  # milliseconds
                "backpressure": {
                    "avg_send_delay": round(avg_delay, 4),
                    "failure_rate": round(failure_rate, 4),
                    "client_count": self.stats["client_count"],
                    "messages_sent": self.stats["messages_sent"],
                    "messages_failed": self.stats["messages_failed"],
                },
            }

            await self.broadcast_metric(metric_data)

            # Send frame data if available
            if self.frame_files:
                await self.broadcast_frame()

            t += 0.1
            await asyncio.sleep(0.125)  # Send data every n seconds

    async def broadcast_frame(self):
        """Broadcast current frame information"""
        if not self.frame_files:
            return

        frame_path = self.frame_files[self.current_frame_index]
        frame_filename = os.path.basename(frame_path)
        frame_dir = os.path.basename(os.path.dirname(frame_path))

        frame_data = {
            "type": "frame",
            "filename": frame_filename,
            "directory": frame_dir,
            "timestamp": int(time.time() * 1000),
            "frame_index": self.current_frame_index,
            "total_frames": len(self.frame_files),
        }

        await self.broadcast_metric(frame_data)

        # Move to next frame
        self.current_frame_index = (self.current_frame_index + 1) % len(
            self.frame_files
        )

    async def handle_client(self, websocket, path):
        await self.register_client(websocket)
        try:
            await websocket.wait_closed()
        finally:
            await self.unregister_client(websocket)

    async def start_server(self):
        self.running = True
        print("Starting WebSocket server on localhost:8765")
        print("Starting HTTP server on localhost:8080")

        # Start the metric generation task
        metric_task = asyncio.create_task(self.generate_noisy_sine_wave())

        # Start HTTP server for serving static files
        app = web.Application()

        # Configure CORS
        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                    allow_methods="*",
                )
            },
        )

        # Serve static files from test-data directory
        app.router.add_static("/frames/", path="test-data", name="frames")

        # Add CORS to all routes
        for route in list(app.router.routes()):
            cors.add(route)

        # Start HTTP server
        http_server = web.AppRunner(app)
        await http_server.setup()
        http_site = web.TCPSite(http_server, "localhost", 17171)
        await http_site.start()

        # Start the WebSocket server
        async with websockets.serve(self.handle_client, "0.0.0.0", 8765):
            print("WebSocket server running on ws://localhost:8765")
            print("HTTP server running on http://localhost:17171")
            print("Frames available at http://localhost:8080/frames/")
            await asyncio.Future()  # Run forever


async def main():
    producer = MetricProducer()
    await producer.start_server()


if __name__ == "__main__":
    asyncio.run(main())
