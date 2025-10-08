<script>
    import {
        stages,
        sedationStageActive,
        measurementStageActive,
    } from "$lib/state.svelte.js";
    import ActiveFish from "$lib/ActiveFish.svelte";
    import Timer from "$lib/Timer.svelte";
    import BinIcon from "$lib/assets/bin-icon.jpeg";

    function toMeasurement() {
        const fish = stages.sedation;
        fish.sedationEndTime = Date.now();
        stages.measurement = fish;
        stages.sedation = null;
    }

    function discard() {
        if (confirm("Are you sure you want to discard this fish?")) {
            stages.sedation = null;
        }
    }

    const iconIdx = $derived(stages.sedation?.iconIdx);
</script>

<div class="stage-container">
    <h2>Sedation</h2>
    <div class="icon-container">
        <img class="icon-img" src={BinIcon} alt="sedation bin" />
    </div>

    {#if sedationStageActive()}
        <ActiveFish {iconIdx} />
        <div class="timer-container">
            <Timer startTime={stages.sedation.cameraEndTime} />
        </div>

        <div class="button-container">
            <div>
                {#if measurementStageActive()}
                    <button class="stg-btn" disabled>Measurement busy</button>
                {:else}
                    <button class="stg-btn move" onclick={toMeasurement}
                        >To measurement</button
                    >
                {/if}
            </div>
            <div>
                <button class="stg-btn disgard" onclick={discard}
                    >Discard</button
                >
            </div>
        </div>
    {:else}
        <p class="waiting">Waiting for fish</p>
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

    .waiting {
        color: #999;
        font-style: italic;
    }

    .timer-container {
    }
</style>
