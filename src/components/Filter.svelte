<script lang="ts">
  import {
    predictions,
    size,
    filteredIndices,
    minPredictionDifference,
    minDiffFromTruth1,
    minDiffFromTruth2,
    model1BrushedExtent,
    model2BrushedExtent,
    gt,
  } from '../stores';
  import { getFilteredIndices } from '../utils';
  import ScentedWidget from './ScentedWidget.svelte';

  let difference = 0;
  let diffFromTruth1 = 0;
  let diffFromTruth2 = 0;

  function onFilter() {
    $minPredictionDifference = difference;
    $minDiffFromTruth1 = diffFromTruth1;
    $minDiffFromTruth2 = diffFromTruth2;
    $filteredIndices = getFilteredIndices(
      $size,
      $minPredictionDifference,
      $model1BrushedExtent,
      $model2BrushedExtent,
      $minDiffFromTruth1,
      $minDiffFromTruth2,
      $gt,
      $predictions
    );
  }
</script>

<div style="display: flex; align-items: center;">
  <label style="margin-right: 5px;">
    DiffInPredictions
    <input
      type="number"
      bind:value={difference}
      style="margin-left: 5px; width: 50%;"
    />
  </label>
  <label style="margin-right: 5px;">
    DiffFromTruth1 DiffFromTruth2
    <div style="display: flex;">
      <input
        type="number"
        bind:value={diffFromTruth1}
        style="margin-left: 5px; width: 50%;"
      />
      <input
        type="number"
        bind:value={diffFromTruth2}
        style="margin-left: 5px; width: 50%;"
      />
    </div>
  </label>
  <label>
    <button
      on:click={onFilter}
      style="padding-left: 10px; padding-right: 10px;"
    >
      Filter
    </button>
  </label>
</div>
