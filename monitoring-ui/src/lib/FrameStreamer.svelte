<script>
  import { onMount, onDestroy } from "svelte";

  let currentFrame = $state(null);
  let frameInfo = $state(null);
  let frameUrl = $state("");

  // Props
  let { data = null } = $props();

  // React to frame data changes
  $effect(() => {
    if (data && data.type === "frame") {
      updateFrame(data);
    }
  });

  function updateFrame(frameData) {
    frameInfo = frameData;
    
    // Construct the URL for the current frame
    if (frameData.directory && frameData.filename) {
      const newFrameUrl = `http://localhost:8080/frames/${frameData.directory}/${frameData.filename}`;
      
      // Only update if it's a different frame
      if (newFrameUrl !== frameUrl) {
        frameUrl = newFrameUrl;
        
        // Preload the image without showing loading state
        const img = new Image();
        img.onload = () => {
          currentFrame = frameUrl;
        };
        img.onerror = () => {
          console.error("Failed to load frame:", frameUrl);
        };
        img.src = frameUrl;
      }
    }
  }

  function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleTimeString();
  }
</script>

<div class="frame-streamer">
  <div class="frame-header">
    <h3>Live Camera Feed</h3>
    {#if frameInfo}
      <div class="frame-info">
        <p>Frame: {frameInfo.frame_index + 1} / {frameInfo.total_frames}</p>
        <p>Time: {formatTimestamp(frameInfo.timestamp)}</p>
        <p>Directory: {frameInfo.directory}</p>
      </div>
    {/if}
  </div>

  <div class="frame-container">
    {#if currentFrame}
      <img src={currentFrame} alt="Camera Frame" class="frame-image" />
    {:else}
      <div class="no-frame">
        <p>No frame data available</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .frame-streamer {
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .frame-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 10px;
  }

  .frame-header h3 {
    margin: 0;
    color: #333;
  }

  .frame-info {
    text-align: right;
    font-size: 0.9em;
    color: #666;
  }

  .frame-info p {
    margin: 2px 0;
  }

  .frame-container {
    position: relative;
    width: 100%;
    max-width: 640px;
    margin: 0 auto;
    border: 2px solid #ddd;
    border-radius: 4px;
    background-color: #000;
    overflow: hidden;
  }

  .frame-image {
    width: 100%;
    height: auto;
    display: block;
  }

  .loading, .no-frame {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #666;
    background-color: #f0f0f0;
  }

  .loading p, .no-frame p {
    margin: 0;
    font-style: italic;
  }

  @media (max-width: 768px) {
    .frame-header {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }

    .frame-info {
      text-align: center;
    }
  }
</style>
