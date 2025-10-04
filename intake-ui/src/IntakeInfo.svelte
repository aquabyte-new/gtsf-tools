<script>
    import { samplingInfo } from "./lib/state.svelte.js";
    import IntakeModal from "./IntakeModal.svelte";

    let showModal = $state(false);

    // Persist samplingInfo to sessionStorage whenever it changes
    $effect(() => {
        sessionStorage.setItem("samplingInfo", JSON.stringify(samplingInfo));
    });
    
    function formatSpecies(species) {
        if (!species) return "";
        return species
            .replace(/_/g, " ")
            .replace(/\b\w/g, c => c.toUpperCase());
    }
</script>

<div class="intake-info">
    <div class="intake-info-header">
        <h3 class="font-bold">Intake Info</h3>
        <span class="edit-btn-container">
            (<button class="edit-btn" onclick={() => showModal = true}>edit</button>)
        </span>
    </div>
    <div><i>Pen ID</i>: {samplingInfo.penId}</div>
    <div><i>Species</i>: {formatSpecies(samplingInfo.species)}</div>
    <div><i>Location</i>: {samplingInfo.location}</div>
</div>

{#if showModal}
    <IntakeModal bind:showModal />
{/if}

<style>
    .intake-info-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;

        h3 {
            margin: 0;
        }
    }

    .edit-btn {
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
