<script>
  import favicon from "$lib/assets/gtsf-icon.svg";
  import "../styles.css";

  import DebugBanner from "$lib/DebugBanner.svelte";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>


{#if import.meta.env.DEV}
  <DebugBanner dev={true} />
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
