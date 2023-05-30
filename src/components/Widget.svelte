<script lang="ts">
  import Filter from './Filter.svelte';
  import SlopeChart from './SlopeChart.svelte';
  import ShapTable from './ShapTable.svelte';
  import { height } from '../stores';
  import BoxPlots from './BoxPlots.svelte';
  let slopeChartWidth = 0;
  let slopeChartHeight = 0;
</script>

<div class="svelte-widget-container" style:height="{$height}px">
  <div
    class="slope-chart"
    bind:clientWidth={slopeChartWidth}
    bind:clientHeight={slopeChartHeight}
  >
    <Filter />
    <SlopeChart width={slopeChartWidth} height={slopeChartHeight} />
  </div>
  <div class="filter-and-table">
    <ShapTable />
    <BoxPlots />
  </div>
</div>

<style>
  .svelte-widget-container {
    box-sizing: border-box;
    width: 100%;
    font-size: 16px;
    border: 1px solid #eeeeee;
    background-color: white;
    color: black;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1em;
  }
  .filter-and-table {
    flex: 1;
    min-width: 0;
  }
  .slope-chart {
    flex: 1;
    height: 90%;
  }
</style>
