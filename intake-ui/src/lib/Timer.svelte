<script>
  import { onMount, onDestroy } from 'svelte';

  let { startTime } = $props();
  
  let t0 = $derived(Math.floor(startTime / 1000) * 1000)
  let elapsed = $state(0);
  let intervalId;

  function updateElapsed() {
    if (t0) {
      elapsed = (Date.now() - t0) / 1000;
    }
  }

  function formatTime(totalSeconds) {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = Math.floor(totalSeconds % 60);
    const milliseconds = Math.floor((totalSeconds % 1) * 10);
    
    const m = `${String(minutes).padStart(0, '0')}`;
    const s = `${String(seconds).padStart(2, '0')}`;
    const ms = `${String(milliseconds)}`;
    return `${m}m ${s}.${ms}s`;
  }

  onMount(() => {
    updateElapsed();
    intervalId = setInterval(updateElapsed, 50);
  });

  onDestroy(() => {
    if (intervalId) {
      clearInterval(intervalId);
    }
  });
</script>

<div class="timer">
  <p>Timer</p>
  {formatTime(elapsed)}
</div>

<style>
  .timer p {
    font-size: 0.8rem;
    margin: 0;
    margin-bottom: 0.2rem;
    font-style: italic;
  }

  .timer {
    font-family: Verdana;
    font-size: 1.5rem;
    color: #333;
    background-color: #e8e8e8;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    border: 1px solid #999;
    display: inline-block;
    letter-spacing: 0.1rem;
    text-align: center;
    min-width: 5rem;
  }
</style>

