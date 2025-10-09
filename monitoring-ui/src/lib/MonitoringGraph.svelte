<script>
  import { onMount, onDestroy, untrack } from "svelte";
  import * as echarts from "echarts";

  let chartContainer;
  let chart;
  let maxDataPoints = 1000; // Keep last 1000 points for history

  // Use $state (not raw) so template reactively updates when counts change
  const classCounts = $state({
    HIGH: 0,
    LOW: 0,
    MEDIUM: 0,
    PARTIAL: 0,
  });

  const lines = {
    HIGH: [],
    LOW: [],
    MEDIUM: [],
    PARTIAL: [],
  };

  // Props
  let { data = null } = $props();

  // React to data changes
  // https://svelte.dev/docs/svelte/$effect#When-not-to-use-$effect
  $effect(() => {
    if (data && chart && data.biomass !== undefined) {
      updateChart(data.createdAt, data.biomass);
    }
  });

  function updateChart(ts, biomassInfo) {
    const detections = biomassInfo.detections;

    detections.forEach((detection) => {
      const className = detection.left.class_name;
      // Use untrack to read the value without creating a reactive dependency
      // This prevents infinite loops in the $effect
      classCounts[className] = untrack(() => classCounts[className]) + 1;
    });

    // Use untrack when reading counts to prevent reactive dependencies
    lines["PARTIAL"].push([ts, untrack(() => classCounts["PARTIAL"])]);
    lines["LOW"].push([ts, untrack(() => classCounts["LOW"])]);
    lines["MEDIUM"].push([ts, untrack(() => classCounts["MEDIUM"])]);
    lines["HIGH"].push([ts, untrack(() => classCounts["HIGH"])]);

    // Keep only last maxDataPoints for each line
    Object.keys(lines).forEach((key) => {
      if (lines[key].length > maxDataPoints) {
        lines[key].shift();
      }
    });

    // Update chart with all 4 series
    chart.setOption({
      series: [
        { data: lines["HIGH"] },
        { data: lines["MEDIUM"] },
        { data: lines["LOW"] },
        { data: lines["PARTIAL"] },
      ],
    });
  }

  onMount(() => {
    // Initialize ECharts
    chart = echarts.init(chartContainer);

    // Set initial chart options
    chart.setOption({
      title: {
        text: "Live Pranker Data - Class Counts",
      },
      tooltip: {
        trigger: "axis",
        formatter: function (params) {
          let result = `Time: ${new Date(params[0].value[0]).toLocaleTimeString()}<br/>`;
          params.forEach((param) => {
            result += `${param.seriesName}: ${param.value[1]}<br/>`;
          });
          return result;
        },
      },
      legend: {
        data: ["HIGH", "MEDIUM", "LOW", "PARTIAL"],
        top: 30,
      },
      xAxis: {
        type: "time",
        name: "Time",
      },
      yAxis: {
        type: "value",
        name: "Count",
      },
      series: [
        {
          name: "HIGH",
          type: "line",
          data: [],
          smooth: true,
          symbol: "none",
          color: "#ff4444",
        },
        {
          name: "MEDIUM",
          type: "line",
          data: [],
          smooth: true,
          symbol: "none",
          color: "#ff9944",
        },
        {
          name: "LOW",
          type: "line",
          data: [],
          smooth: true,
          symbol: "none",
          color: "#44ff44",
        },
        {
          name: "PARTIAL",
          type: "line",
          data: [],
          smooth: true,
          symbol: "none",
          color: "#4444ff",
        },
      ],
    });
  });

  onDestroy(() => {
    if (chart) {
      chart.dispose();
    }
  });
</script>

<div>
  <div class="card">
    <div>HIGH: {classCounts["HIGH"]}</div>
    <div>MEDIUM: {classCounts["MEDIUM"]}</div>
    <div>LOW: {classCounts["LOW"]}</div>
    <div>PARTIAL: {classCounts["PARTIAL"]}</div>
  </div>
  <div class="card">
    <div bind:this={chartContainer} style="width: 100%; height: 400px;"></div>
  </div>
</div>

<style>
</style>
