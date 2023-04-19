<script>
  import { DataHandler } from '@vincjo/datatables';
  import { shap1, shap2, shapD, features } from '../stores';
  import { defaultFormat } from '../vis-utils.ts';
  import { scaleDiverging } from 'd3-scale';
  import { max } from 'd3-array';
  import { interpolateRdYlGn } from 'd3-scale-chromatic';
  let selectedShapValues = $shapD;
  $: handler = new DataHandler(selectedShapValues, { rowsPerPage: 20 });
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

<style>
  table {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
  }
</style>
