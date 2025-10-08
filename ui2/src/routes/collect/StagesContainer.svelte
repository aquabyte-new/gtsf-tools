<script>
  import CameraStage from './CameraStage.svelte';
  import SedationStage from './SedationStage.svelte';
  import MeasurementStage from './MeasurementStage.svelte';
</script>

<div class="main">
    <CameraStage />
    <SedationStage />
    <MeasurementStage />
</div>

<style>
  .main {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
    width: 100%;
    height: 78vh;
  }
</style>