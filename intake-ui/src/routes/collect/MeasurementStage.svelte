<script>
  import {
    stages,
    saveFish,
    measurementStageActive,
  } from "$lib/state.svelte.js";
  import {
    isWeightValid,
    isLengthValid,
    isWidthValid,
    isBreadthValid,
  } from "$lib/validation.js";
  import ActiveFish from "$lib/ActiveFish.svelte";
  import BoardIcon from "$lib/assets/measuring-icon-2.jpeg";
  import { saveFishToBackend } from "$lib/export.svelte.js";

  const activeFish = $derived(stages.measurement);

  // Form state.
  let weight = $state("");
  let length = $state("");
  let width = $state("");
  let breadth = $state("");
  let circumference = $state("");
  let notes = $state("");

  let isSaving = $state(false);

  // submit entry and release fish
  async function log() {
    const check = (msg) => confirm(msg + ", are you sure you want to submit?");
    if (!isWeightValid(weight) && !check("Weight is unusual")) return;
    if (!isLengthValid(weight, length) && !check("Length is ususual")) return;
    if (!isWidthValid(weight, width) && !check("Width is unusual")) return;
    if (!isBreadthValid(weight, breadth) && !check("Breadth is unusual"))
      return;

    const completedFish = {
      ...stages.measurement,
      measurementEnd: Date.now(),
      weightG: weight,
      lengthMm: length,
      widthMm: width,
      breadthMm: breadth,
      circumferenceMm: circumference,
      notes: notes,
    };

    // Save to backend first
    isSaving = true;
    const saved = await saveFishToBackend(completedFish);
    isSaving = false;

    if (!saved) {
      // Backend save failed - don't update local state
      return;
    }

    // Add to local entries for history/CSV export
    saveFish(completedFish);

    stages.measurement = null;

    resetForm();
  }

  function discard() {
    if (confirm("Are you sure you want to discard this fish?")) {
      stages.measurement = null;
      resetForm();
    }
  }

  function resetForm() {
    weight = "";
    length = "";
    width = "";
    breadth = "";
    notes = "";
  }

  const iconIdx = $derived(stages.measurement?.iconIdx);

  // Minimal validations before submitting.
  function isPosNum(x) {
    return x !== "" && !isNaN(x) && x > 0;
  }
  const weightOk = $derived(isPosNum(weight));
  const lengthOk = $derived(isPosNum(length));
  const canSubmit = $derived(weightOk && lengthOk && !isSaving);
</script>

<div class="stage-container">
  <h2>Measurement</h2>
  <div class="icon-container">
    <img class="icon-img" src={BoardIcon} alt="measuring icon" />
  </div>

  {#if measurementStageActive()}
    <ActiveFish {iconIdx} />

    <h3>Data entry</h3>
    <form>
      <div class="form-group">
        <label for="weight">Weight:*</label>
        <input
          type="number"
          id="weight"
          bind:value={weight}
          step="1"
          placeholder="grams"
          class:invalid={!weightOk}
        />
      </div>
      <div class="form-group">
        <label for="length">Length:*</label>
        <input
          type="number"
          id="length"
          bind:value={length}
          step="1"
          placeholder="mm"
          class:invalid={!lengthOk}
        />
      </div>
      <div class="form-group">
        <label for="width">Width:</label>
        <input
          type="number"
          id="length"
          bind:value={width}
          step="1"
          placeholder="mm"
        />
      </div>
      <div class="form-group">
        <label for="breadth">Breadth:</label>
        <input
          type="number"
          id="length"
          bind:value={breadth}
          step="1"
          placeholder="mm"
        />
      </div>
      <p>Notes</p>
      <textarea
        class="notes"
        id="notes"
        bind:value={notes}
        placeholder="Add any notes on welfare or sampling here"
      ></textarea>
    </form>

    <div class="button-container">
      <div>
        <button class="stg-btn move" onclick={log} disabled={!canSubmit}>
          {isSaving ? 'Saving...' : 'Submit and release'}
        </button>
      </div>
      <div>
        <button class="stg-btn disgard" onclick={discard}>Discard</button>
      </div>
    </div>
  {:else}
    <p class="waiting">Waiting for fish</p>
  {/if}
</div>

<style>
  .stage-container {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .button-container {
    margin-top: auto;
    display: flex;
    justify-content: flex-end;
    flex-direction: column;
  }

  .waiting {
    color: #999;
    font-style: italic;
  }

  .form-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    gap: 1rem;
  }

  .form-group label {
    text-align: left;
  }

  .form-group input {
    text-align: right;
    font-size: 1rem;
    padding: 0.2rem;
    width: 10rem;
    border: 1px solid #000000;
  }

  .form-group input.invalid {
    border-color: #ff4444;
  }

  .notes {
    width: 100%;
    height: 4rem;
    vertical-align: top;
    resize: vertical;
  }

  h3 {
    margin-top: 0;
  }
</style>
