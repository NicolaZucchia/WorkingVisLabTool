<script lang="ts">
  import Filter from './Filter.svelte';
  import SlopeChart from './SlopeChart.svelte';
  import ShapTable from './ShapTable.svelte';
  import { height } from '../stores';
  let difference = 0;
  function onChangeDifference(event){
    difference = event.detail;
  }
</script>

<div class="svelte-widget-container" style:height="{$height}px">
  <div>
    <Filter on:filter={onChangeDifference}/>
    <ShapTable />
  </div>
  <SlopeChart width={$height} height={$height} {difference} />
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
  }
</style>
