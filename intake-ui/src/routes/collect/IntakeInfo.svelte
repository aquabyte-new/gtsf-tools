<script>
    import { samplingInfo } from "$lib/state.svelte.js";

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
        <h3 class="font-bold">Metadata</h3>
    </div>
    <div><i>Name</i>: {samplingInfo.name}</div>
    <div><i>Pen ID</i>: {samplingInfo.penId}</div>
    <div><i>Species</i>: {formatSpecies(samplingInfo.species)}</div>
    <div><i>Location</i>: {samplingInfo.location}</div>
</div>

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

</style>
