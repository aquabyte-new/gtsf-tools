<script>
  import { samplingInfo } from "./lib/state.svelte.js";
  import HistorySidebar from "./HistorySidebar.svelte";
  import StagesContainer from "./StagesContainer.svelte";
  
  const today = new Date().toISOString().slice(0, 10)
  let editingPenId = $state(false);
</script>

<main>
  <div>
    <h1>GTSF Collection</h1>
    <h2>Pen ID: {samplingInfo.penId}</h2>
  </div>

  <div>
    Today: {today}
  </div>

  <div>
    <span>Pen ID: </span>
    {#if editingPenId}
      <input 
        type="text" 
        bind:value={samplingInfo.penId}
        onblur={() => editingPenId = false}
      />
    {:else}
      {samplingInfo.penId}
      (<button class="edit-btn" onclick={() => editingPenId = true}>edit</button>)
    {/if}
  </div>

  <div class="container">
    <HistorySidebar />
    <StagesContainer />
  </div>
</main>


<style>
  .container {
    display: flex;
    flex-direction: row;
    gap: 2rem;
    margin-top: 2rem;
  }

  input[type="text"] {
    padding: 0.25rem 0.25rem;
    border: 1px solid #ccc;
    width: 5rem;
  }

  .edit-btn {
    width: fit-content;
    padding: 0;
    background: none;
    border: none;
    color: #4a90e2;
    font-size: inherit;
    cursor: pointer;
    text-decoration: none;
  }

  .edit-btn:hover {
    text-decoration: underline;
  }
</style>
