<script>
  import { DataHandler } from '@vincjo/datatables';
  import { shap1, shap2, shapD, features, filteredIndices } from '../stores';
  import { defaultFormat } from '../vis-utils.ts';
  import { scaleDiverging } from 'd3-scale';
  import { max } from 'd3-array';
  import { interpolateRdYlGn } from 'd3-scale-chromatic';
  import RowCount from './RowCount.svelte';
  import Pagination from './Pagination.svelte';
  import Filter from './Filter.svelte';
  let selectedShapValues = $shapD;
  $: filteredSelectedShapValues = $filteredIndices.map(
    (i) => selectedShapValues[i]
  );
  $: handler = new DataHandler(filteredSelectedShapValues, { rowsPerPage: 15 });
  $: rows = handler.getRows();
  $: absMaxShap = max(selectedShapValues.flat(), (d) => Math.abs(d)) ?? 0;
  $: color = scaleDiverging()
    .domain([-absMaxShap, 0, absMaxShap])
    .interpolator(interpolateRdYlGn);
</script>

<div>
  <div>
    <label>
      <input
        type="radio"
        bind:group={selectedShapValues}
        name="shapD"
        value={$shapD}
      />
      Shap Difference
    </label>
    <label>
      <input
        type="radio"
        bind:group={selectedShapValues}
        name="shap1"
        value={$shap1}
      />
      Shap Model 1
    </label>
    <label>
      <input
        type="radio"
        bind:group={selectedShapValues}
        name="shap2"
        value={$shap2}
      />
      Shap Model 2
    </label>
  </div>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          {#each $features as f}
            <th>{f}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each $rows as row}
          <tr>
            {#each $features as f, i}
              <td style:background={color(row[i])}>{defaultFormat(row[i])}</td>
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
  }
  th,
  td {
    text-align: right;
    padding: 0.125em 0.25em;
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
  }
  footer {
    border-top: 1px solid #e0e0e0;
  }
</style>
