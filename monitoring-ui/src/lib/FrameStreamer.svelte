<script>
  import { onMount, onDestroy } from "svelte";

  let currentFrame = $state(null);
  let frameInfo = $state(null);
  let ts = $state(null);
  let frameUrl = $state("");

  // Props
  let { data = null } = $props();

  // React to frame data changes
  $effect(() => {
    if (data && data.leftThumb !== undefined) {
      updateFrame(data.createdAt, data.leftThumb);
    }
  });

  function updateFrame(ts, frameData) {
    frameInfo = frameData;
    ts = ts;
    
    // Construct the URL for the current frame
    if (frameData.directory && frameData.filename) {
      const newFrameUrl = `http://localhost:17171/${frameData.directory}/${frameData.filename}`;
      
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

<div class="card">
  <div class="card-header">
    <div class="title">Live Camera Feed (left camera)</div>
    {#if frameInfo}
      <div class="frame-info">
        <p>Directory: {frameInfo.directory}</p>
      </div>
    {/if}
  </div>

    {#if currentFrame}
    <div class="frame-container">
        <img src={currentFrame} alt="Camera Frame" class="frame-image" />
    </div>
    {:else}
      <p><i>Waiting for images...</i></p>
    {/if}
</div>

<style>
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 0.1rem;
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

  .no-frame {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #666;
    background-color: #f0f0f0;
  }

  .no-frame p {
    margin: 0;
    font-style: italic;
  }
</style>
