<script>
  import { onMount, onDestroy } from "svelte";
  import * as echarts from "echarts";

  let chartContainer;
  let chart;
  let maxDataPoints = 1000; // Keep last 1000 points for history

  const classCounts = {
    'HIGH': 0,
    'LOW': 0,
    'MEDIUM': 0,
    'PARTIAL': 0,
  };

  const lines = {
    'HIGH': [],
    'LOW': [],
    'MEDIUM': [],
    'PARTIAL': [],
  };


  // Props
  let { data = null } = $props();

  // React to data changes
  // https://svelte.dev/docs/svelte/$effect#When-not-to-use-$effect
  $effect(() => {
    if (data && chart && data.type === "detections") {
      updateChart(data);
    }
  });

  function updateChart(metricData) {
    const ts = metricData.timestamp;
    const detections = metricData.value;
    console.log(detections);
    
    detections.forEach(detection => {
      const className = detection.left.class_name;
      classCounts[className]++;
    });
    
    lines['PARTIAL'].push([ts, classCounts['PARTIAL']]);
    lines['LOW'].push([ts, classCounts['LOW']]);
    lines['MEDIUM'].push([ts, classCounts['MEDIUM']]);
    lines['HIGH'].push([ts, classCounts['HIGH']]);

    // Keep only last maxDataPoints for each line
    Object.keys(lines).forEach(key => {
      if (lines[key].length > maxDataPoints) {
        lines[key].shift();
      }
    });

    // Update chart with all 4 series
    chart.setOption({
      series: [
        { data: lines['HIGH'] },
        { data: lines['MEDIUM'] },
        { data: lines['LOW'] },
        { data: lines['PARTIAL'] },
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
          params.forEach(param => {
            result += `${param.seriesName}: ${param.value[1]}<br/>`;
          });
          return result;
        },
      },
      legend: {
        data: ['HIGH', 'MEDIUM', 'LOW', 'PARTIAL'],
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
