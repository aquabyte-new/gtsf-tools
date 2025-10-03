<script>
    import {
        plainFish,
        prettyFish,
        getRandomFishIcon,
    } from "./fishIcon.svelte.js";

    let { usePlain = false, iconIdx = null } = $props();
    
    function getIcon() {
        if (usePlain) {
            return plainFish;
        } else if (iconIdx !== null) {
            return prettyFish[iconIdx];
        } else {
            return getRandomFishIcon();
        }
    }
</script>

<img src={getIcon()} alt="fish" />

<style>
    img {
        width: 2rem;
    }
</style>
