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
    if (data && chart) {
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

    // Update peaks
    if (isLow && metricData.val > 9.5) {
      isLow = false;
      peaks = peaks + 1;
    } else if (metricData.val < 0) {
      isLow = true;
    }

    // Update backpressure metrics
    if (metricData.backpressure) {
      backpressure = metricData.backpressure;
    }
  }

  onMount(() => {
    // Initialize ECharts
    chart = echarts.init(chartContainer);

    // Set initial chart options
    chart.setOption({
      title: {
        text: "Noisy Sine Wave Live Data",
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
        min: -15,
        max: 15,
      },
      series: [
        {
          name: "noisy_sine_wave",
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
  <div>
    <h1>Peaks: {peaks}</h1>
  </div>

  <div class="chart-container">
    <div bind:this={chartContainer} style="width: 100%; height: 400px;"></div>
  </div>

  <div class="metrics">
    <h4>Backpressure Metrics:</h4>
    <p>Clients: {backpressure.client_count}</p>
    <p>Avg Send Delay: {backpressure.avg_send_delay}s</p>
    <p>Failure Rate: {(backpressure.failure_rate * 100).toFixed(2)}%</p>
    <p>Messages Sent: {backpressure.messages_sent}</p>
    <p>Messages Failed: {backpressure.messages_failed}</p>
  </div>
</div>

<style>
  .monitoring-graph {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .stats {
    display: flex;
    gap: 30px;
    align-items: flex-start;
  }

  .chart-container {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 20px;
  }

  .metrics {
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    min-width: 250px;
  }

  .metrics h4 {
    margin-top: 0;
  }

  .metrics p {
    margin: 5px 0;
  }
</style>
