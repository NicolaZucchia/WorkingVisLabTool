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

<div style="display: flex; align-items: center;">
  <label style="margin-right: 5px;">
    DiffInPredictions
    <input type="number" bind:value={difference} style="margin-left: 5px;" />
  </label>
  <label style="margin-right: 5px;">
    DiffFromTruth
    <input type="number" bind:value={diffFromTruth} style="margin-left: 5px;" />
  </label>
  <button on:click={onFilter} style="padding-left: 10px; padding-right: 10px;"
    >Filter</button
  >
</div>
