<script>
    import {
        stages,
        cameraStageActive,
        sedationStageActive,
    } from "./lib/state.svelte.js";

    function reset() {
        stages.camera = null;
    }

    function addFish() {
        const ts = Date.now();
        stages.camera = {
            cameraStartTime: ts,
            fishId: String(ts).slice(-4),
        };
        console.log(stages.camera);
    }

    function toSedation() {
        if (sedationStageActive()) {
            alert("Sedation full");
            return;
        }

        stages.camera.cameraEndTime = Date.now();
        stages.sedation = stages.camera;
        stages.camera = null;
    }

    const activeFish = $derived(stages.camera);
</script>

<div>
    <h2>Camera</h2>

    {#if cameraStageActive()}
        <div>Current fish: {activeFish.fishId}</div>

        {#if sedationStageActive()}
            <div>
                <button class="move-blocked">Sedation full</button>
            </div>
        {:else}
            <div>
                <button class="move" onclick={toSedation}>To sedation</button>
            </div>
        {/if}

        <div>
            <button class="reset" onclick={reset}>Reset</button>
        </div>
    {:else}
        <p class="waiting">Waiting for fish</p>
        <button class="add" onclick={addFish}>Add fish</button>
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
