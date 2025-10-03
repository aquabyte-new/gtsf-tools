<script>
  import { entries } from './lib/state.svelte.js';
</script>

<div class="sidebar">
  <h2>History</h2>
  {#if entries.length > 0}
    <div>
    Total fish: {entries.length}
    </div>
    <div class="history-list">
      {#each entries as fish}
        <div class="history-item">
          <div class="history-detail">
            <strong>Fish {fish.fishId}</strong>
          </div>
          <div class="history-timestamp">
            {fish.cameraStartTime}
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <p class="empty-message">No submissions yet</p>
  {/if}
</div>

<style>
  .sidebar {
    width: 250px;
    border-right: 1px solid #e0e0e0;
    padding-right: 1.5rem;
  }
  
  .history-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .history-item {
    padding: 0.75rem;
    background-color: #f8f9fa;
    border-radius: 4px;
    border: 1px solid #e0e0e0;
  }
  
  .history-detail {
    margin-bottom: 0.25rem;
    font-size: 0.95rem;
  }
  
  .history-detail strong {
    color: #555;
  }
  
  .history-timestamp {
    margin-top: 0.5rem;
    font-size: 0.8rem;
    color: #888;
  }
  
  .empty-message {
    color: #999;
    font-style: italic;
  }
</style>

