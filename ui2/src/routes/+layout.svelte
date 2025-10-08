<script>
  import favicon from "$lib/assets/gtsf-icon.svg";
  import "../styles.css";

  import DebugBanner from "$lib/DebugBanner.svelte";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<DebugBanner />

{#if import.meta.env.DEV}
  <div class="banner dev">
    <div class="banner-title">DEVELOPMENT MODE</div>
    <div>
      Backend API: <a
        href="{import.meta.env.VITE_API_URL}/docs"
        target="_blank"
      >
        {import.meta.env.VITE_API_URL}
      </a>
    </div>
  </div>
{/if}

{@render children?.()}

<style>
  .banner {
    background-color: #56abff;
    color: rgb(0, 0, 0);
    padding: 0.5rem;
    text-align: center;
    margin: 0rem;
    
    &.dev {
      background-color: #ffa7a7;
    }
  }

  .banner-title {
    text-transform: uppercase;
    font-weight: bold;
  }
</style>
