<script>
    import {
        stages,
        cameraStageActive,
        sedationStageActive,
    } from "./lib/state.svelte.js";
    import HHIcon from "./assets/hh-real.png";
    import ActiveFish from "./lib/ActiveFish.svelte";
    import { getUnusedFishIconIdx } from "./lib/fishIcon.svelte.js";

    function reset() {
        if (confirm("Are you sure you want to discard this fish?")) {
            stages.camera = null;
        }
    }

    function addFish() {
        stages.camera = {
            cameraStartTime: Date.now(),
            fishId: crypto.randomUUID().slice(0, 4),
            iconIdx: getUnusedFishIconIdx(),
        };
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

    const iconIdx = $derived(stages.camera?.iconIdx);
</script>

<div class="stage-container">
    <h2>Camera</h2>
    <div class="icon-container">
        <img class="icon-img" src={HHIcon} alt="hammerhead" />
    </div>

    {#if cameraStageActive()}
        <ActiveFish {iconIdx} />
        <div class="button-container">
            {#if sedationStageActive()}
                <button class="stg-btn busy">Sedation busy</button>
            {:else}
                <button class="stg-btn move" onclick={toSedation}>To sedation</button>
            {/if}

            <div>
                <button class="stg-btn disgard" onclick={reset}>Reset</button>
            </div>
        </div>
    {:else}
        <p class="waiting-msg">Waiting for fish</p>
        <div class="button-container">
            <button class="stg-btn add" onclick={addFish}>Add fish</button>
        </div>
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

    .waiting-msg {
        color: #999;
        font-style: italic;
    }

    .icon-container {
        width: 100%;
        align-items: center;
    }

    .icon-img {
        height: 70px;
    }
</style>
