<script>
  import { stages, samplingInfo, entries, clearAppState } from "./lib/state.svelte.js";
  import HistorySidebar from "./HistorySidebar.svelte";
  import StagesContainer from "./StagesContainer.svelte";
  import IntakeInfo from "./IntakeInfo.svelte";

  // Persist session state
  $effect(() => {
    sessionStorage.setItem("entries", JSON.stringify(entries));
    sessionStorage.setItem("samplingInfo", JSON.stringify(samplingInfo));
    sessionStorage.setItem("stages", JSON.stringify(stages));
  });
</script>

<main>
  <div class="header">
    <h1 class="header-title">GTSF Collection</h1>
    <button class="clear-button" onclick={clearAppState}>Clear</button>
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
  
  .header-title {
    margin-right: 1rem;
  }
</style>
