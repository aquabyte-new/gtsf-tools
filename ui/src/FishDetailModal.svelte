<script>
  import FishIcon from "./lib/FishIcon.svelte";

  let { fish = null, onClose } = $props();

  function formatTimestamp(timestamp) {
    if (!timestamp) return "N/A";
    return new Date(timestamp).toLocaleString();
  }

  function formatDuration(start, end) {
    if (!start || !end) return "N/A";
    const durationMs = end - start;
    const seconds = Math.floor(durationMs / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  }

  function handleBackdropClick(e) {
    if (e.target === e.currentTarget) {
      onClose();
    }
  }
</script>

{#if fish}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="modal-backdrop" onclick={handleBackdropClick}>
    <div class="modal-content">
      <div class="modal-header">
        <h2>Fish Details</h2>
        <button class="close-button" onclick={onClose}>×</button>
      </div>

      <div class="modal-body">
        <div class="detail-section">
          <div class="fish-icon-display">
            <FishIcon iconIdx={fish.iconIdx} />
          </div>
        </div>

        <div class="detail-section">
          <h3>Identity</h3>
          <div class="detail-row">
            <span class="label">Fish ID:</span>
            <span class="value">{fish.fishId}</span>
          </div>
        </div>

        <div class="detail-section">
          <h3>Measurements</h3>
          <div class="detail-row">
            <span class="label">Weight:</span>
            <span class="value">{fish.weight ?? "N/A"} {fish.weight ? "g" : ""}</span>
          </div>
          <div class="detail-row">
            <span class="label">Length:</span>
            <span class="value">{fish.length ?? "N/A"} {fish.length ? "mm" : ""}</span>
          </div>
          <div class="detail-row">
            <span class="label">Width:</span>
            <span class="value">{fish.width ?? "N/A"} {fish.width ? "mm" : ""}</span>
          </div>
          <div class="detail-row">
            <span class="label">Breadth:</span>
            <span class="value">{fish.breadth ?? "N/A"} {fish.breadth ? "mm" : ""}</span>
          </div>
        </div>

        <div class="detail-section">
          <h3>Timeline</h3>
          <div class="detail-row">
            <span class="label">Camera Start:</span>
            <span class="value">{formatTimestamp(fish.cameraStartTime)}</span>
          </div>
          <div class="detail-row">
            <span class="label">Camera End:</span>
            <span class="value">{formatTimestamp(fish.cameraEndTime)}</span>
          </div>
          <div class="detail-row">
            <span class="label">Camera Duration:</span>
            <span class="value">{formatDuration(fish.cameraStartTime, fish.cameraEndTime)}</span>
          </div>
          <div class="detail-row">
            <span class="label">Sedation End:</span>
            <span class="value">{formatTimestamp(fish.sedationEndTime)}</span>
          </div>
          <div class="detail-row">
            <span class="label">Sedation Duration:</span>
            <span class="value">{formatDuration(fish.cameraEndTime, fish.sedationEndTime)}</span>
          </div>
          <div class="detail-row">
            <span class="label">Measurement End:</span>
            <span class="value">{formatTimestamp(fish.measurementEndTime)}</span>
          </div>
          <div class="detail-row">
            <span class="label">Measurement Duration:</span>
            <span class="value">{formatDuration(fish.sedationEndTime, fish.measurementEndTime)}</span>
          </div>
        </div>

        {#if fish.notes}
          <div class="detail-section">
            <h3>Notes</h3>
            <div class="notes-content">{fish.notes}</div>
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    background-color: white;
    border-radius: 8px;
    max-width: 600px;
    max-height: 90vh;
    width: 90%;
    display: flex;
    flex-direction: column;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #e0e0e0;
  }

  .modal-header h2 {
    margin: 0;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    padding: 0;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-button:hover {
    color: #666;
  }

  .modal-body {
    padding: 1rem;
    overflow-y: auto;
  }

  .detail-section {
    margin-bottom: 1.5rem;
  }

  .detail-section h3 {
    margin-top: 0;
    margin-bottom: 0.75rem;
    font-size: 1.1rem;
    color: #333;
  }

  .detail-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f0f0;
  }

  .detail-row:last-child {
    border-bottom: none;
  }

  .label {
    font-weight: 500;
    color: #666;
  }

  .value {
    color: #333;
  }

  .notes-content {
    padding: 0.75rem;
    background-color: #f8f9fa;
    border-radius: 4px;
    white-space: pre-wrap;
  }

  .fish-icon-display {
    display: flex;
    justify-content: center;
    padding: 1rem 0;
  }
</style>

