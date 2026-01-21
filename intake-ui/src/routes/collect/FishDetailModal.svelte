<script>
  import FishIcon from "$lib/FishIcon.svelte";
  import { samplingInfo, entries } from "$lib/state.svelte.js";
  import {
    isWeightValid,
    isLengthValid,
    isWidthValid,
    isBreadthValid,
  } from "$lib/validation.js";

  const apiUrl = `${import.meta.env.VITE_API_URL}/api`;

  let { fish = null, onClose } = $props();

  let isEditing = $state(false);
  let isSaving = $state(false);
  let editedWeight = $state('');
  let editedLength = $state('');
  let editedWidth = $state('');
  let editedBreadth = $state('');
  let editedNotes = $state('');

  // Validation state
  const weightValid = $derived(isWeightValid(editedWeight ? parseFloat(editedWeight) : null));
  const lengthValid = $derived(isLengthValid(
    editedWeight ? parseFloat(editedWeight) : null,
    editedLength ? parseFloat(editedLength) : null
  ));
  const widthValid = $derived(isWidthValid(
    editedWeight ? parseFloat(editedWeight) : null,
    editedWidth ? parseFloat(editedWidth) : null
  ));
  const breadthValid = $derived(isBreadthValid(
    editedWeight ? parseFloat(editedWeight) : null,
    editedBreadth ? parseFloat(editedBreadth) : null
  ));

  // Initialize edit values when fish changes
  $effect(() => {
    if (fish) {
      editedWeight = fish.weightG?.toString() || '';
      editedLength = fish.lengthMm?.toString() || '';
      editedWidth = fish.widthMm?.toString() || '';
      editedBreadth = fish.breadthMm?.toString() || '';
      editedNotes = fish.notes || '';
    }
  });

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

  function formatTime(timestamp) {
    if (!timestamp) return "N/A";
    return new Date(timestamp).toLocaleTimeString();
  }

  function handleBackdropClick(e) {
    if (e.target === e.currentTarget) {
      onClose();
    }
  }

  function startEditing() {
    isEditing = true;
  }

  function cancelEditing() {
    isEditing = false;
    // Reset to original values
    editedWeight = fish.weightG?.toString() || '';
    editedLength = fish.lengthMm?.toString() || '';
    editedWidth = fish.widthMm?.toString() || '';
    editedBreadth = fish.breadthMm?.toString() || '';
    editedNotes = fish.notes || '';
  }

  async function saveChanges() {
    const weight = editedWeight ? parseFloat(editedWeight) : null;
    const length = editedLength ? parseFloat(editedLength) : null;
    const width = editedWidth ? parseFloat(editedWidth) : null;
    const breadth = editedBreadth ? parseFloat(editedBreadth) : null;
    const notes = editedNotes || null;

    // Validation with confirmation dialogs (same as MeasurementStage)
    const check = (msg) => confirm(msg + ", are you sure you want to save?");
    if (!isWeightValid(weight) && !check("Weight is unusual")) return;
    if (!isLengthValid(weight, length) && !check("Length is unusual")) return;
    if (!isWidthValid(weight, width) && !check("Width is unusual")) return;
    if (!isBreadthValid(weight, breadth) && !check("Breadth is unusual")) return;

    // Save to backend
    const collectionId = samplingInfo.collectionId;
    if (collectionId) {
      isSaving = true;
      try {
        const response = await fetch(`${apiUrl}/samples/${collectionId}/${fish.fishId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            weightG: weight,
            lengthMm: length,
            widthMm: width,
            breadthMm: breadth,
            notes: notes
          }),
        });

        if (!response.ok) {
          const text = await response.text();
          throw new Error(`HTTP ${response.status}: ${text}`);
        }
      } catch (error) {
        console.error('Failed to update fish:', error);
        alert(`Failed to update fish: ${error.message}`);
        isSaving = false;
        return;
      }
      isSaving = false;
    }

    // Update local state
    const fishIndex = entries.findIndex(f => f.fishId === fish.fishId);
    if (fishIndex !== -1) {
      entries[fishIndex] = {
        ...entries[fishIndex],
        weightG: weight,
        lengthMm: length,
        widthMm: width,
        breadthMm: breadth,
        notes: notes
      };
      
      // Update the fish prop reference
      fish.weightG = weight;
      fish.lengthMm = length;
      fish.widthMm = width;
      fish.breadthMm = breadth;
      fish.notes = notes;
    }
    
    isEditing = false;
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
            <FishIcon iconIdx={fish.iconIdx} size="4rem" weight={fish.weightG}/>
          </div>
        </div>

        <div class="detail-section">
          <div class="section-header">
            <h3>Identity</h3>
            {#if !isEditing}
              <button class="edit-button" onclick={startEditing}>Edit</button>
            {/if}
          </div>
          <div class="detail-row">
            <span class="label">Fish ID:</span>
            <span class="value">{fish.fishId}</span>
          </div>
          <div class="detail-row">
            <span class="label">Species:</span>
            <span class="value">{samplingInfo.species}</span>
          </div>
          <div class="detail-row notes-row-display">
            <span class="label">Notes:</span>
            {#if isEditing}
              <textarea 
                id="notes-input"
                bind:value={editedNotes} 
                class="edit-textarea"
                placeholder="Add any notes"
              ></textarea>
            {:else if fish.notes}
              <span class="value notes-value">{fish.notes}</span>
            {:else}
              <span class="value notes-empty">No notes</span>
            {/if}
          </div>
        </div>

        <div class="detail-section">
          <div class="section-header">
            <h3>Measurements</h3>
            {#if !isEditing}
              <button class="edit-button" onclick={startEditing}>Edit</button>
            {/if}
          </div>
          
          {#if isEditing}
            <div class="edit-form">
              <div class="edit-row">
                <label for="weight-input" class="edit-label">Weight (g):</label>
                <input 
                  id="weight-input"
                  type="number" 
                  step="1" 
                  bind:value={editedWeight} 
                  class="edit-input"
                  class:invalid={editedWeight && !weightValid}
                  placeholder="Enter weight"
                />
              </div>
              <div class="edit-row">
                <label for="length-input" class="edit-label">Length (mm):</label>
                <input 
                  id="length-input"
                  type="number" 
                  step="1" 
                  bind:value={editedLength} 
                  class="edit-input"
                  class:invalid={editedLength && !lengthValid}
                  placeholder="Enter length"
                />
              </div>
              <div class="edit-row">
                <label for="width-input" class="edit-label">Width (mm):</label>
                <input 
                  id="width-input"
                  type="number" 
                  step="1" 
                  bind:value={editedWidth} 
                  class="edit-input"
                  class:invalid={editedWidth && !widthValid}
                  placeholder="Enter width"
                />
              </div>
              <div class="edit-row">
                <label for="breadth-input" class="edit-label">Breadth (mm):</label>
                <input 
                  id="breadth-input"
                  type="number" 
                  step="1" 
                  bind:value={editedBreadth} 
                  class="edit-input"
                  class:invalid={editedBreadth && !breadthValid}
                  placeholder="Enter breadth"
                />
              </div>
              <div class="edit-actions">
                <button class="save-button" onclick={saveChanges} disabled={isSaving}>
                  {isSaving ? 'Saving...' : 'Save'}
                </button>
                <button class="cancel-button" onclick={cancelEditing} disabled={isSaving}>Cancel</button>
              </div>
            </div>
          {:else}
            <div class="detail-row">
              <span class="label">Weight:</span>
              <span class="value">{fish.weightG ?? "N/A"} {fish.weightG ? "g" : ""}</span>
            </div>
            <div class="detail-row">
              <span class="label">Length:</span>
              <span class="value">{fish.lengthMm ?? "N/A"} {fish.lengthMm ? "mm" : ""}</span>
            </div>
            <div class="detail-row">
              <span class="label">Width:</span>
              <span class="value">{fish.widthMm ?? "N/A"} {fish.widthMm ? "mm" : ""}</span>
            </div>
            <div class="detail-row">
              <span class="label">Breadth:</span>
              <span class="value">{fish.breadthMm ?? "N/A"} {fish.breadthMm ? "mm" : ""}</span>
            </div>
          {/if}
        </div>

        <div class="detail-section">
          <h3>Timeline</h3>
          <div class="timeline">
            <div class="timeline-labels">
              <div class="stage-label">
                <span class="label-name">Camera</span>
                <span class="label-duration">{formatDuration(fish.captureStart, fish.captureEnd)}</span>
              </div>
              <div class="stage-label">
                <span class="label-name">Sedation</span>
                <span class="label-duration">{formatDuration(fish.captureEnd, fish.sedationEnd)}</span>
              </div>
              <div class="stage-label">
                <span class="label-name">Measurement</span>
                <span class="label-duration">{formatDuration(fish.sedationEnd, fish.measurementEnd)}</span>
              </div>
            </div>
            
            <div class="timeline-bar">
              <div class="timeline-segment camera"></div>
              <div class="timeline-segment sedation"></div>
              <div class="timeline-segment measurement"></div>
            </div>
            
            <div class="timeline-times">
              <span class="time-marker">{formatTime(fish.captureStart)}</span>
              <span class="time-marker">{formatTime(fish.captureEnd)}</span>
              <span class="time-marker">{formatTime(fish.sedationEnd)}</span>
              <span class="time-marker">{formatTime(fish.measurementEnd)}</span>
            </div>
          </div>
        </div>

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

  .notes-row-display {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .notes-row-display .edit-textarea {
    width: 100%;
  }

  .notes-value {
    white-space: pre-wrap;
  }

  .notes-empty {
    color: #999;
    font-style: italic;
  }

  .fish-icon-display {
    display: flex;
    justify-content: center;
  }

  .timeline {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .timeline-labels {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
  }

  .stage-label {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
  }

  .label-name {
    font-weight: 600;
    font-size: 0.9rem;
    color: #333;
  }

  .label-duration {
    font-size: 0.85rem;
    color: #666;
  }

  .timeline-bar {
    display: flex;
    height: 0.5rem;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #ddd;
  }

  .timeline-segment {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .timeline-segment.camera {
    background-color: #90caf9;
  }

  .timeline-segment.sedation {
    background-color: #ffb74d;
  }

  .timeline-segment.measurement {
    background-color: #81c784;
  }

  .timeline-times {
    display: flex;
    justify-content: space-between;
  }

  .time-marker {
    font-size: 0.8rem;
    color: #666;
    font-family: monospace;
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .edit-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.85rem;
  }

  .edit-button:hover {
    background-color: #0056b3;
  }

  .edit-form {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .edit-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .edit-label {
    font-weight: 500;
    color: #666;
    min-width: 100px;
  }

  .edit-input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
  }

  .edit-input:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }

  .edit-input.invalid {
    border-color: #ff4444;
  }

  .edit-textarea {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
    min-height: 4rem;
    resize: vertical;
    font-family: inherit;
  }

  .edit-textarea:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }

  .edit-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
    justify-content: flex-end;
  }

  .save-button {
    background-color: #28a745;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .save-button:hover {
    background-color: #218838;
  }

  .cancel-button {
    background-color: #6c757d;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .cancel-button:hover {
    background-color: #545b62;
  }
</style>

