<script>
    import { stages, sedationStageActive, measurementStageActive } from './lib/state.svelte.js';
    
    function toMeasurement() {
        const fish = stages.sedation;
        fish.sedationEndTime = Date.now()
        stages.measurement = fish;
        stages.sedation = null;
    }
</script>

<div>
    <h2>Sedation</h2>
    {#if sedationStageActive()}
        <div>Current fish: {stages.sedation.fishId}</div>
        
        {#if measurementStageActive()}
            <div>
                <button class="move-blocked">Measurement full</button>
            </div>
        {:else}
            <div>
                <button class="move" onclick={toMeasurement}>To measurement</button>
            </div>
        {/if}
        <div>
            <button class="reset">Reset timer</button>
        </div>
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
    
    .move-blocked {
        background-color: #c6c6c6;
    }
</style>