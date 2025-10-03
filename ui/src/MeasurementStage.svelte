<script>
  import {
    stages,
    saveFish,
    measurementStageActive,
  } from "./lib/state.svelte.js";

  const activeFish = $derived(stages.measurement);

  // submit entry and release fish
  function log() {
    stages.measurement.measurementEndTime = Date.now();
    const fishnum = saveFish(stages.measurement, 200);
    stages.measurement = null;
    return fishnum;
  }

  // new stuff
  let weight = "";
  let length = "";
  let width = "";
  let breadth = "";
  let notes = "";
  let onSubmit;
</script>

<div>
  <h2>Measurements</h2>
  {#if measurementStageActive()}
    <div>Current fish: {activeFish.fishId}</div>
    <div>
      <button class="move" onclick={log}>Submit and release</button>
    </div>

    <h3>Data entry</h3>
    <form>
      <div class="form-group">
        <label for="weight">Weight:</label>
        <input
          type="number"
          id="weight"
          bind:value={weight}
          step="1"
          placeholder="weight in grams"
        />
      </div>
      <div class="form-group">
        <label for="length">Length:</label>
        <input
          type="number"
          id="length"
          bind:value={length}
          step="1"
          placeholder="length in mm"
        />
      </div>
      <div class="form-group">
        <label for="width">Width:</label>
        <input
          type="number"
          id="length"
          bind:value={width}
          step="1"
          placeholder="width in mm"
        />
      </div>
      <div class="form-group">
        <label for="breadth">Breadth:</label>
        <input
          type="number"
          id="length"
          bind:value={breadth}
          step="1"
          placeholder="breadth in mm"
        />
      </div>
      <p>Notes</p>
      <input
        class="notes"
        type="text"
        id="notes"
        bind:value={notes}
        placeholder="Add any notes on welfare or sampling here"
      />
    </form>
  {:else}
    <p class="waiting">Waiting for fish</p>
  {/if}
</div>

<style>
  .reset {
    background-color: #ff4444;
  }
  .waiting {
    color: #999;
    font-style: italic;
  }
  .form-group {
    margin-bottom: 0.5rem;
  }

  .notes {
    width: 100%;
    height: 4rem;
  }
</style>
