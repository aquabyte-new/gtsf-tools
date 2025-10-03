<script>
  import {
    stages,
    saveFish,
    measurementStageActive,
  } from "./lib/state.svelte.js";
  import ActiveFish from "./lib/ActiveFish.svelte";
  import BoardIcon from "./assets/measuring.png";

  const activeFish = $derived(stages.measurement);

  // submit entry and release fish
  function log() {
    stages.measurement.measurementEndTime = Date.now();
    const fishnum = saveFish(stages.measurement, 200);
    stages.measurement = null;
    return fishnum;
  }
  
  function discard() {
    if (confirm("Are you sure you want to discard this fish?")) {
      stages.measurement = null;
    }
  }

  // new stuff
  let weight = "";
  let length = "";
  let width = "";
  let breadth = "";
  let notes = "";
  let onSubmit;

  const iconIdx = $derived(stages.measurement?.iconIdx);
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

    <div class="button-container">
      <button class="stg-btn move" onclick={log}>Submit and release</button>
      <button class="stg-btn disgard" onclick={discard}>Discard</button>
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
  }

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

  .icon-img {
    height: 70px;
  }
</style>
