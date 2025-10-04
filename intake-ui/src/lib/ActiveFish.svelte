<script>
    import FishIcon from "./FishIcon.svelte";
    let { iconIdx = null } = $props();
</script>

<div>Active fish: <FishIcon iconIdx={iconIdx} /></div>

<style>
    div {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>