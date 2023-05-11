<script lang="ts">
  import {
    predictions,
    size,
    filteredIndices,
    minPredictionDifference,
    minDiffFromTruth,
    model1BrushedExtent,
    model2BrushedExtent,
    gt,
  } from '../stores';
  import { getFilteredIndices } from '../utils';

  let difference = 0;
  let diffFromTruth = 0;

  function onFilter() {
    $minPredictionDifference = difference;
    $minDiffFromTruth = diffFromTruth;
    $filteredIndices = getFilteredIndices(
      $size,
      $minPredictionDifference,
      $model1BrushedExtent,
      $model2BrushedExtent,
      $minDiffFromTruth,
      $gt,
      $predictions
    );
  }
</script>

<div>
  <label>
    Difference
    <input type="number" bind:value={difference} />
  </label>
  <label>
    DiffFromTruth
    <input type="number" bind:value={diffFromTruth} />
  </label>
  <button on:click={onFilter}> Filter </button>
</div>
