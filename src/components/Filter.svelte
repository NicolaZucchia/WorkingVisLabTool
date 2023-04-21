<script lang="ts">
  import {
    predictions,
    size,
    filteredIndices,
    minPredictionDifference,
    model1BrushedExtent,
    model2BrushedExtent,
  } from '../stores';
  import { getFilteredIndices } from '../utils';

  let difference = 0;

  function onFilter() {
    $minPredictionDifference = difference;
    $filteredIndices = getFilteredIndices(
      $size,
      $minPredictionDifference,
      $model1BrushedExtent,
      $model2BrushedExtent,
      $predictions
    );
  }
</script>

<div>
  <label>
    Difference
    <input type="number" bind:value={difference} />
  </label>
  <button on:click={onFilter}> Filter </button>
</div>
