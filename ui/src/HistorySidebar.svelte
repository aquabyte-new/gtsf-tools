<script>
  import { entries } from './lib/state.svelte.js';
  import FishIcon from './lib/FishIcon.svelte';
  import FishDetailModal from './FishDetailModal.svelte';

  let selectedFish = $state(null);

  function formatTimestamp(timestamp) {
    if (!timestamp) return "N/A";
    return new Date(timestamp).toLocaleString();
  }

  function openFishDetail(fish) {
    selectedFish = fish;
  }

  function closeModal() {
    selectedFish = null;
  }
</script>

<div class="sidebar">
  <h3>History</h3>
  {#if entries.length > 0}
    <div>
    Total fish: {entries.length}
    </div>
    <div class="history-list">
      {#each entries.slice().reverse() as fish, index}
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div class="history-item" onclick={() => openFishDetail(fish)}>
          <div class="history-header">
            <FishIcon usePlain={true} />
            <strong>Fish {entries.length - index}</strong>
          </div>
          <div class="history-detail">
            {formatTimestamp(fish.cameraStartTime)}
          </div>
          <div class="history-detail">
            Weight: {fish.weight ?? "nan"}
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <p class="empty-message">No submissions yet</p>
  {/if}
</div>

<FishDetailModal fish={selectedFish} onClose={closeModal} />

<style>
  h3 {
    margin-top: 0;
    margin-bottom: 0.5rem;
  }
  
  .sidebar {
    display: flex;
    flex-direction: column;
  }
  
  .history-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: calc(100vh - 380px);
    overflow-y: auto;
  }
  
  .history-item {
    padding: 0.75rem;
    background-color: #f8f9fa;
    border-radius: 4px;
    border: 1px solid #e0e0e0;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s;
  }

  .history-item:hover {
    background-color: #e9ecef;
    border-color: #999;
  }

  .history-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .history-header strong {
    font-size: 0.95rem;
    color: #333;
  }
  
  .history-detail {
    font-size: 0.85rem;
    color: #666;
    margin-bottom: 0.25rem;
  }
  
  .empty-message {
    color: #999;
    font-style: italic;
  }
</style>

