<script>
  import { onMount, onDestroy } from "svelte";
  import { WebSocketClient } from "./lib/websocket.svelte.js";
  import MonitoringGraph from "./lib/MonitoringGraph.svelte";
  import FrameStreamer from "./lib/FrameStreamer.svelte";
  
  const WS_URL = import.meta.env.VITE_WS_URL;

  let websocketClient;
  let connectionStatus = $state("disconnected");
  let latestData = $state(null);

  function handleMessage(data) {
    latestData = data;
  }

  function handleStatusChange(status) {
    connectionStatus = status;
  }

  function getStatusMessage() {
    switch (connectionStatus) {
      case "connected":
        return "Connected";
      case "connecting":
        return "Connecting...";
      case "disconnected":
        return "Disconnected";
      case "error":
        return "Connection Error - Retrying...";
      default:
        return "Unknown Status";
    }
  }

  function getStatusClass() {
    switch (connectionStatus) {
      case "connected":
        return "status-connected";
      case "connecting":
        return "status-connecting";
      case "disconnected":
        return "status-disconnected";
      case "error":
        return "status-error";
      default:
        return "status-unknown";
    }
  }

  onMount(() => {
    websocketClient = new WebSocketClient("ws://localhost:8765");
    websocketClient.on("message", handleMessage);
    websocketClient.on("statusChange", handleStatusChange);
    websocketClient.connect();
  });

  onDestroy(() => {
    if (websocketClient) {
      websocketClient.disconnect();
    }
  });
</script>

<main>
  <h1>GTSF Monitoring</h1>

  <!-- <div class="connection-status"> -->
  <div class="card">
    <h3>
      Camera Connection Status: <span class={getStatusClass()}
        >{getStatusMessage()}</span
      >
    </h3>
  </div>

  <!-- WebSocket Client is now managed in JavaScript -->

  <!-- Monitoring Components -->
  {#if connectionStatus === "connected"}
    <div class="display-grid">
      <MonitoringGraph data={latestData} />
      <FrameStreamer data={latestData} />
      <div class="debug">
        <h4>Raw data:</h4>
        <pre>{JSON.stringify(latestData, null, 2)}</pre>
      </div>
    </div>
  {:else if connectionStatus === "connecting"}
  {:else}
    <div class="card error">
      <p>Connection failed. Attempting to reconnect every 5 seconds...</p>
      <p>Make sure the WebSocket server is running on ws://localhost:8765</p>
    </div>
  {/if}
</main>

<style>
  h1 {
    margin-left: 0.5rem;
  }
  h3 {
    margin: 0;
  }

  .status-connected {
    color: #28a745;
    font-weight: bold;
  }

  .status-connecting {
    color: #ffc107;
    font-weight: bold;
  }

  .status-disconnected {
    color: #6c757d;
    font-weight: bold;
  }

  .status-error {
    color: #dc3545;
    font-weight: bold;
  }

  .status-unknown {
    color: #6c757d;
    font-weight: bold;
  }

  .display-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .debug {
    h4 {
      margin-top: 0;
    }
    
    pre {
      margin: 0;
      padding: 1rem;
      background-color: #d2d2d2;
      border-radius: 8px;
    }
  }
</style>
