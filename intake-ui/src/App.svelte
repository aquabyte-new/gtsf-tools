<script>
  import {
    stages,
    samplingInfo,
    entries,
    clearAppState,
  } from "./lib/state.svelte.js";
  import HistorySidebar from "./HistorySidebar.svelte";
  import StagesContainer from "./StagesContainer.svelte";
  import IntakeInfo from "./IntakeInfo.svelte";
  import { exportCSV, saveToBackend } from "./lib/export.svelte.js";

  // Persist session state
  $effect(() => {
    sessionStorage.setItem("entries", JSON.stringify(entries));
    sessionStorage.setItem("samplingInfo", JSON.stringify(samplingInfo));
    sessionStorage.setItem("stages", JSON.stringify(stages));
  });
  
  function clear() {
    if (confirm("Are you sure you want to delete all data?")) {
      clearAppState();
    }
  }
</script>

<main>
  <div class="header">
    <h1 class="header-title">GTSF Collection</h1>
    <button class="export-btn" onclick={exportCSV}>Export</button>
    <button class="save-btn" onclick={saveToBackend}>Save</button>
    <button class="clear-btn" onclick={clear}>Delete all</button>
  </div>

  <div class="container">
    <div class="left-sidebar">
      <IntakeInfo />
      <HistorySidebar />
    </div>
    <StagesContainer />
  </div>
</main>

<style>
  .container {
    display: flex;
    flex-direction: row;
    gap: 2rem;
  }

  .left-sidebar {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    width: 14rem;
    flex-shrink: 0;
    border-right: 1px solid #e0e0e0;
    padding-right: 1rem;
  }

  .header {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .clear-btn {
    margin-left: 1rem;
    cursor: pointer;
    background-color: #ff7575;
    border: 1px solid;
    border-radius: 0rem;
  }

  .export-btn {
    margin-left: 2rem;
    cursor: pointer;
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 0rem;
  }

  .save-btn {
    margin-left: 1rem;
    cursor: pointer;
    background-color: #2b9cff;
    border: 1px solid #e0e0e0;
    border-radius: 0rem;
  }
</style>
