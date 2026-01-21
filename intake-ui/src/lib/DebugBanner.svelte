<script>
    let { dev = false } = $props();
</script>

<div class="banner">
    {#if dev}
        <div class="banner-title">DEVELOPMENT MODE</div>
    {/if}
    <div>
        Backend API:
        <a href="{import.meta.env.VITE_API_URL}/docs" target="_blank">
            {import.meta.env.VITE_API_URL}
        </a>
    </div>
</div>

<style>
    .banner {
        background-color: #56abff;
        color: rgb(0, 0, 0);
        padding: 0.5rem;
        text-align: center;
        margin: 0rem;
    }

    .banner-title {
        text-transform: uppercase;
        font-weight: bold;
    }
</style>
