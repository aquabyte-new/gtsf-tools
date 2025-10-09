<script>
  import { onMount, onDestroy } from "svelte";
  import * as echarts from "echarts";

  let chartContainer;
  let chart;
  let dataPoints = [];
  let maxDataPoints = 1000; // Keep last 1000 points for history

  let peaks = $state(0);
  let isLow = $state(true);
  let backpressure = $state({
    avg_send_delay: 0,
    failure_rate: 0,
    client_count: 0,
    messages_sent: 0,
    messages_failed: 0,
  });

  // Props
  let { data = null } = $props();

  // React to data changes
  $effect(() => {
    if (data && chart && data.type !== "frame") {
      updateChart(data);
    }
  });

  function updateChart(metricData) {
    // Add new data point
    dataPoints.push([metricData.timestamp, metricData.val]);

    // Keep only last maxDataPoints
    if (dataPoints.length > maxDataPoints) {
      dataPoints.shift();
    }

    // Update chart
    chart.setOption({
      series: [
        {
          data: dataPoints,
        },
      ],
    });
  }

  onMount(() => {
    // Initialize ECharts
    chart = echarts.init(chartContainer);

    // Set initial chart options
    chart.setOption({
      title: {
        text: "Live Pranker Data",
      },
      tooltip: {
        trigger: "axis",
        formatter: function (params) {
          const data = params[0];
          return `Time: ${new Date(data.value[0]).toLocaleTimeString()}<br/>Value: ${data.value[1]}`;
        },
      },
      xAxis: {
        type: "time",
        name: "Time",
      },
      yAxis: {
        type: "value",
        name: "Value",
      },
      series: [
        {
          name: "live_pranker_data",
          type: "line",
          data: [],
          smooth: true,
          symbol: "none",
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

<div class="monitoring-graph">
  <div class="chart-container">
    <div bind:this={chartContainer} style="width: 100%; height: 400px;"></div>
  </div>
</div>

<style>
  .monitoring-graph {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .chart-container {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 20px;
  }
</style>
