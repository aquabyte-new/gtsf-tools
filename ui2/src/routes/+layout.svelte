<script>
  import favicon from "$lib/assets/gtsf-icon.svg";
  import "../styles.css";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

{#if import.meta.env.DEV}
  <div class="dev-banner">
    <div class="dev-banner-title">DEVELOPMENT MODE</div>
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
  .dev-banner {
    background-color: #ffa7a7;
    color: rgb(0, 0, 0);
    padding: 0.5rem;
    text-align: center;
    margin: 0rem;
  }
  .dev-banner-title {
    text-transform: uppercase;
    font-weight: bold;
  }
</style>
