<script>
    import {
        plainFish,
        prettyFish,
        getRandomFishIcon,
    } from "./fishIcon.svelte.js";

    let {
        usePlain = false,
        iconIdx = null,
        size = "2rem",
        weight = null,
    } = $props();

    function getIcon() {
        if (usePlain) {
            return plainFish;
        } else if (iconIdx != null && prettyFish[iconIdx]) {
            return prettyFish[iconIdx];
        } else {
            return getRandomFishIcon();
        }
    }
</script>

<div class="fish-icon-container">
    <img src={getIcon()} alt="fish" style="width: {size};" />
    {#if weight}
        <div class="weight">{weight}g</div>
    {/if}
</div>

<style>
    .fish-icon-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 1rem;
        font-style: italic;
    }
</style>
