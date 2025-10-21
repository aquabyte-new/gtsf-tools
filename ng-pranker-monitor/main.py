import asyncio
import json
import time
from pathlib import Path
from typing import Set
from collections import defaultdict

import websockets
from loguru import logger


BIND_ADDRESS = "0.0.0.0"
WEBSOCKET_PORT = 8765

LIVE_DIR = Path("/ssd/captures-live")
MIN_RANKER_SCORE = 1e-5


def latest_dir() -> Path:
    dirs = LIVE_DIR.glob("*-*-*T*:*:*Z")
    return sorted(dirs)[-1]


class Producer:
    def __init__(self):
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.running = False

    async def broadcast(self, data):
        if self.clients:
            message = json.dumps(data)
            
            try:
                await asyncio.gather(
                    *[client.send(message) for client in self.clients],
                    return_exceptions=True,
                )
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
            
        else:
            # logger.debug("No clients to broadcast to")
            pass

    async def generate(self):
        latest = None
        while self.running:
            try:
                # Get the latest directory and make sure we don't double count.
                new_dir = latest_dir()
                if new_dir == latest:
                    logger.debug("No new directory found, skipping.")
                    await asyncio.sleep(0.01)
                    continue
                latest = new_dir

                logger.info("New directory found.")
                
                # Start with empty message.
                capture_msg = dict(
                    createdAt=int(time.time() * 1000),
                    capturedAt=latest.name,
                )

                # Left frame info.
                left_thumb = latest / "left_frame.resize_512_512.jpg"
                if left_thumb.exists():
                    logger.info("Left thumb exists.")
                    capture_msg["leftThumb"] = dict(
                        filename=left_thumb.name,
                        directory=left_thumb.parent.name,
                    )
                
                # Right frame info.
                right_thumb = latest / "right_frame.resize_512_512.jpg"
                if right_thumb.exists():
                    capture_msg["rightThumb"] = dict(
                        filename=right_thumb.name,
                        directory=right_thumb.parent.name,
                    )
                
                # Biomass detections info.
                biom_detection = latest / "biomass_detections.json"
                if biom_detection.exists():
                    detections = json.loads(biom_detection.read_text())

                    capture_msg["biomass"] = dict(
                        detections=detections,
                        classCounts=defaultdict(int),
                        ranks=[],
                        goodCrops=0,
                    )
                    
                    for detection in detections:
                        name = detection['left']['class_name']
                        max_rank = max(rank or 0 for rank in detection['biomass_ranker'])
                        capture_msg["biomass"]["classCounts"][name] += 1
                        capture_msg["biomass"]["ranks"].append(max_rank)
                        capture_msg["biomass"]["goodCrops"] += (max_rank >= MIN_RANKER_SCORE)

                if 'biomass' in capture_msg:
                    await self.broadcast(capture_msg)

                sleep_ms = 10
                await asyncio.sleep(sleep_ms / 1e3)
            except Exception as e:
                logger.error(f"Error in generate loop: {e}", exc_info=True)
                await asyncio.sleep(1)  # Wait a bit before retrying

    async def handle_client(self, websocket, path):
        logger.info("New client connected.")
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            logger.info("Client disconnected.")
            self.clients.discard(websocket)

    async def start_server(self):
        self.running = True

        # Start the metric generation task
        logger.info("Starting metric generation...")
        metric_task = asyncio.create_task(self.generate())

        # Start the WebSocket server
        async with websockets.serve(self.handle_client, BIND_ADDRESS, WEBSOCKET_PORT):
            logger.info(
                f"WebSocket server running on ws://{BIND_ADDRESS}:{WEBSOCKET_PORT}"
            )
            await asyncio.Future()  # Run forever


async def main():
    logger.info("Creating producer...")
    producer = Producer()

    logger.info("Starting server...")
    await producer.start_server()


if __name__ == "__main__":
    logger.info("Starting ng-pranker-monitor...")
    asyncio.run(main())
