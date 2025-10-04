<script>
  import { onMount, onDestroy } from 'svelte';

  let { startTime } = $props();
  
  let t0 = $derived(Math.floor(startTime / 1000) * 1000)
  
  let elapsed = $state(0);
  let intervalId;

  function updateElapsed() {
    if (t0) {
      elapsed = Math.floor((Date.now() - t0) / 1000);
    }
  }

  function formatTime(totalSeconds) {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  }

  onMount(() => {
    updateElapsed();
    intervalId = setInterval(updateElapsed, 100);
  });

  onDestroy(() => {
    if (intervalId) {
      clearInterval(intervalId);
    }
  });
</script>

<h4>Timer</h4>
<div class="timer">
  {formatTime(elapsed)}
</div>

<style>
  .timer {
    font-family: 'Courier New', monospace;
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
    background-color: #e8e8e8;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    border: 2px solid #999;
    display: inline-block;
    letter-spacing: 0.1rem;
    text-align: center;
    min-width: 5rem;
  }
</style>

