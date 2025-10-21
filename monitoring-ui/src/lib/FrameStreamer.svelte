<script>
  import { onMount, onDestroy } from "svelte";

  let currentFrame = $state(null);
  let frameInfo = $state(null);
  let ts = $state(null);
  let frameUrl = $state("");
  let detections = $state([]);
  let canvasEl = $state(null);
  let imgEl = $state(null);
  let imageLoaded = $state(false);

  // Props
  let { data = null } = $props();

  // React to frame data changes
  $effect(() => {
    if (data && data.leftThumb !== undefined) {
      updateFrame(data.createdAt, data.leftThumb);

      // Update detections
      if (data && data.biomass !== undefined) {
        detections = data.biomass.detections || [];
        console.log("Received detections:", detections.length, detections);
      } else {
        console.log("No detections received:");
        console.log($inspect(data));
      }
    }
  });

  // Draw bounding boxes when image or detections change
  $effect(() => {
    if (imageLoaded && detections.length > 0 && imgEl && canvasEl) {
      drawBoundingBoxes();
    } else if (canvasEl) {
      console.log("Clearing canvas because no detections or image not loaded");
      // Clear canvas if no detections
      const ctx = canvasEl.getContext("2d");
      ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
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
        imageLoaded = false; // Reset loaded state for new frame

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

  function onImageLoad() {
    console.log("Image loaded");
    if (canvasEl && imgEl) {
      // Set canvas size to match image display size
      canvasEl.width = imgEl.clientWidth;
      canvasEl.height = imgEl.clientHeight;
      imageLoaded = true; // Mark image as loaded
      // drawBoundingBoxes will be called by the effect
    }
  }

  function drawBoundingBoxes() {
    if (!canvasEl || !imgEl || !detections || detections.length === 0) {
      console.log("drawBoundingBoxes skipped:", {
        canvasEl: !!canvasEl,
        imgEl: !!imgEl,
        detections: detections?.length,
      });
      return;
    }

    const ctx = canvasEl.getContext("2d");
    ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);

    // Original source image dimensions
    const SOURCE_WIDTH = 2448;
    const SOURCE_HEIGHT = 2024;

    // Get thumbnail dimensions (actual loaded image)
    const thumbWidth = imgEl.naturalWidth;
    const thumbHeight = imgEl.naturalHeight;

    // Get display dimensions
    const displayWidth = imgEl.clientWidth;
    const displayHeight = imgEl.clientHeight;

    console.log("Drawing bounding boxes:", {
      detections: detections.length,
      thumbSize: `${thumbWidth}x${thumbHeight}`,
      displaySize: `${displayWidth}x${displayHeight}`,
      canvasSize: `${canvasEl.width}x${canvasEl.height}`,
    });

    // Calculate scale factors from source to thumbnail
    const sourceToThumbX = thumbWidth / SOURCE_WIDTH;
    const sourceToThumbY = thumbHeight / SOURCE_HEIGHT;

    // Calculate scale factors from thumbnail to display
    const thumbToDisplayX = displayWidth / thumbWidth;
    const thumbToDisplayY = displayHeight / thumbHeight;

    // Combined scale factors from source to display
    const scaleX = sourceToThumbX * thumbToDisplayX;
    const scaleY = sourceToThumbY * thumbToDisplayY;

    detections.forEach((detection) => {
      if (!detection.left) return;

      const { x0, y0, x1, y1, class_name } = detection.left;

      // Scale coordinates from source image to display size
      const scaledX0 = x0 * scaleX;
      const scaledY0 = y0 * scaleY;
      const scaledX1 = x1 * scaleX;
      const scaledY1 = y1 * scaleY;
      const width = scaledX1 - scaledX0;
      const height = scaledY1 - scaledY0;

      // Set style based on class_name
      let strokeStyle = "grey";
      let lineWidth = 1;

      switch (class_name) {
        case "PARTIAL":
          strokeStyle = "grey";
          lineWidth = 1;
          break;
        case "LOW":
          strokeStyle = "white";
          lineWidth = 1;
          break;
        case "MEDIUM":
          strokeStyle = "blue";
          lineWidth = 2;
          break;
        case "HIGH":
          strokeStyle = "green";
          lineWidth = 2;
          break;
      }

      // Draw bounding box
      ctx.strokeStyle = strokeStyle;
      ctx.lineWidth = lineWidth;
      ctx.strokeRect(scaledX0, scaledY0, width, height);

      // Draw label
      ctx.fillStyle = strokeStyle;
      ctx.font = "12px sans-serif";
      const label = `${class_name} ${(detection.left.conf * 100).toFixed(0)}%`;
      const textMetrics = ctx.measureText(label);
      const textHeight = 14;

      // Draw background for label
      ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
      ctx.fillRect(
        scaledX0,
        scaledY0 - textHeight - 2,
        textMetrics.width + 4,
        textHeight + 2,
      );

      // Draw label text
      ctx.fillStyle = strokeStyle;
      ctx.fillText(label, scaledX0 + 2, scaledY0 - 4);
    });
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
        <p>Detections: {detections.length}</p>
      </div>
    {/if}
  </div>

  {#if currentFrame}
    <div class="frame-container">
      <img
        bind:this={imgEl}
        src={currentFrame}
        alt="Camera Frame"
        class="frame-image"
        onload={onImageLoad}
      />
      <canvas bind:this={canvasEl} class="bounding-box-canvas"></canvas>
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
    width: 620px;
    height: 512px;
    margin: 0 auto;
    border: 2px solid #ddd;
    border-radius: 4px;
    background-color: #000;
    overflow: hidden;
  }

  .frame-image {
    width: 620px;
    height: 512px;
    display: block;
    object-fit: fill;
  }

  .bounding-box-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }
</style>
