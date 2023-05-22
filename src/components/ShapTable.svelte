<script>
  import { DataHandler } from '@vincjo/datatables';
  import { shap1, shap2, shapD, features, filteredIndices } from '../stores';
  import { defaultFormat } from '../vis-utils.ts';
  import { scaleDiverging } from 'd3-scale';
  import { max } from 'd3-array';
  //import { interpolateRdYlGn } from 'd3-scale-chromatic';
  import { interpolateCool, interpolateWarm } from 'd3-scale-chromatic';
  import RowCount from './RowCount.svelte';
  import Pagination from './Pagination.svelte';
  import Filter from './Filter.svelte';
  import { descending, sum } from 'd3-array';
  let selectedShapValues = $shapD;
  let numFeatures = selectedShapValues[0].shap.length;
  $: filteredSelectedShapValues = $filteredIndices
    .map((i) => selectedShapValues[i])
    .sort((a, b) => descending(a.shapAbsSum, b.shapAbsSum));

  function featureOrdering(selectedShapValues) {
    let column_sum = new Array(features.length).fill(0);
    for (let i = 0; i < numFeatures; i++) {
      column_sum[i] = sum(selectedShapValues, (d) => Math.abs(d.shap[i]));
    }
    return column_sum
      .map((d, i) => {
        return { value: d, index: i };
      })
      .sort((a, b) => b.value - a.value)
      .map((d) => d.index);
  }

  function permutation(v, index) {
    let result = index.map((i) => v[i]);
    return result;
  }

  $: shapVar = filteredSelectedShapValues.map((d) => d.shap);
  $: handler = new DataHandler(shapVar, { rowsPerPage: 20 });
  $: rows = handler.getRows();
  $: absMaxShap = max(shapVar.flat(), (d) => Math.abs(d)) ?? 0;
  $: color = scaleDiverging()
    .domain([-absMaxShap, 0, absMaxShap])
    .range(['#00BFFF', '#FFFFE0', '#FFA07A']);

  let cur_perm = featureOrdering(selectedShapValues);
</script>

<div>
  <div style="display: flex;">
    <div style="margin-right: 10px;">
      <label>
        <input
          type="radio"
          bind:group={selectedShapValues}
          name="shapD"
          value={$shapD}
        />
        ShapDiff
      </label>
      <label>
        <input
          type="radio"
          bind:group={selectedShapValues}
          name="shap1"
          value={$shap1}
        />
        ShapM1
      </label>
      <label>
        <input
          type="radio"
          bind:group={selectedShapValues}
          name="shap2"
          value={$shap2}
        />
        ShapM2
      </label>
    </div>
    <div style="display: flex;">
      <div style="display: flex; align-items: center;">
        <span
          style="background-color: #00BFFF; width: 20px; height: 20px; margin-right: 5px;"
        />
        <span>1</span>
      </div>
      <div style="display: flex; align-items: center;">
        <span
          style="background-color: #FFFFE0; width: 20px; height: 20px; margin-right: 5px;"
        />
        <span>0</span>
      </div>
      <div style="display: flex; align-items: center;">
        <span
          style="background-color: #FFA07A; width: 20px; height: 20px; margin-right: 5px;"
        />
        <span>-1</span>
      </div>
    </div>
  </div>

  <div class="table-container">
    <table>
      <thead>
        <tr>
          {#each permutation($features, cur_perm) as f}
            <th class="long-string" title={f}>{f}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each $rows as row, rowIndex}
          <tr>
            {#each permutation(row, cur_perm) as f, columnIndex}
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <td
                style="background-color: {color(f)}"
                on:click={() => console.log(row)}
              >
                {defaultFormat(f)}
                <!--(row[columnIndex])-->
              </td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

<footer>
  <RowCount {handler} />
  <Pagination {handler} />
</footer>

<style>
  table {
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    table-layout: fixed;
  }

  th {
    padding: 0.125em 0.25em;
    writing-mode: vertical-lr;
    transform: rotate(-180deg);
    max-height: 5em;
    max-width: 50px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow-wrap: break-word;
    font-weight: normal;
  }

  td {
    text-align: right;
    padding: 0.0625em 0.125em; /* Adjusted padding for smaller cell size */
    font-size: 0;
    height: 1em; /* Added to control cell height */
  }

  .long-string {
    max-width: 100%;
    overflow: hidden;
  }

  .table-container {
    overflow-x: auto;
  }

  footer {
    height: 48px;
    padding: 0 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e0e0e0;
  }
</style>
