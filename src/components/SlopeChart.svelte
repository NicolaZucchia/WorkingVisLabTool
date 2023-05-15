<script lang="ts">
  import {
    predictions,
    minPrediction,
    maxPrediction,
    size,
    minPredictionDifference,
    minDiffFromTruth,
    gt,
    model1BrushedExtent,
    model2BrushedExtent,
  } from '../stores';
  import { scaleLinear, scalePoint } from 'd3-scale';
  import { getFilteredIndices } from '../utils';
  import { shapD, filteredIndices } from '../stores';
  import { select } from 'd3-selection';
  import { brushY } from 'd3-brush';
  import type { Selection } from 'd3-selection';
  import type { D3BrushEvent } from 'd3-brush';
  import { max } from 'd3-array';
  let selectedShapValues = $shapD;
  export let width: number;
  export let height: number;

  const margin = { top: 20, right: 40, bottom: 40, left: 40 };
  const tickSize = 6;

  $: x = scalePoint<number>()
    .domain([0, 1])
    .range([margin.left, width - margin.right]);

  $: y = scaleLinear()
    .domain([$minPrediction, $maxPrediction])
    .nice()
    .range([height - margin.bottom, margin.top]);

  $: linesToShow = getFilteredIndices(
    $size,
    $minPredictionDifference,
    [-Infinity, Infinity],
    [-Infinity, Infinity],
    $minDiffFromTruth,
    $gt,
    $predictions
  );

  function getDiffFromGT(predictions: number[], gt: number[]): number[] {
    let vecDist = [];
    for (let i = 0; i < gt.length; i++) {
      vecDist.push(predictions[i] - gt[i]);
    }
    return vecDist;
  }

  $: vecDist0 = getDiffFromGT($predictions[0], $gt);
  $: vecDist1 = getDiffFromGT($predictions[1], $gt);

  $: maxDistGT = Math.max(
    max(vecDist0, Math.abs) ?? 0,
    max(vecDist1, Math.abs) ?? 0
  );

  $: lengthScale = scaleLinear().domain([0, maxDistGT]).range([0, 40]);

  function getLineLength(value) {
    return lengthScale(Math.abs(value));
  }

  //$: gBrush = select('#brush').node();

  function handleClick(i: number) {
    console.log(`Values of row ${i}:`, selectedShapValues[i].shap);
    console.log('Ground truth for that:', $gt[i]);
    console.log('Prediction for that:', $predictions[0][i], $predictions[1][i]);
  }

  function handleBrush(
    this: SVGGElement,
    { selection }: D3BrushEvent<undefined>
  ) {
    const isModel1 = this.id === 'model1-axis';
    if (selection === null) {
      if (isModel1) {
        $model1BrushedExtent = [-Infinity, Infinity];
      } else {
        $model2BrushedExtent = [-Infinity, Infinity];
      }
    } else {
      const [y1, y2] = selection as [number, number];
      const max = y.invert(y1);
      const min = y.invert(y2);
      if (isModel1) {
        $model1BrushedExtent = [min, max];
      } else {
        $model2BrushedExtent = [min, max];
      }
    }
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

  const brushWidth = 20;
  $: brush = brushY<undefined>()
    .extent([
      [-brushWidth / 2, margin.top],
      [brushWidth / 2, height - margin.bottom],
    ])
    //.on('brush', (e) => handleBrush(e.selection))
    .on('start brush end', handleBrush);

  let group: SVGGElement | undefined = undefined;
  let selection: Selection<SVGGElement, undefined, SVGElement, undefined>;

  $: if (group && brush) {
    selection = select(group).selectAll('.axis');
    selection.call(brush);
  }
</script>

<svg {width} {height}>
  <g bind:this={group}>
    <!-- lines -->
    <g>
      {#each linesToShow as i}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <line
          x1={x(0)}
          x2={x(1)}
          y1={y($predictions[0][i])}
          y2={y($predictions[1][i])}
          fill="none"
          stroke={$filteredIndices.includes(i) ? 'steelblue' : 'grey'}
          opacity={'0.1'}
          on:click={(event) => handleClick(i)}
        />
      {/each}
    </g>
    <g>
      {#each linesToShow as i}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <line
          x1={x(0) - getLineLength(vecDist0[i])}
          x2={x(0)}
          y1={y($predictions[0][i])}
          y2={y($predictions[0][i])}
          fill="none"
          stroke={vecDist0[i] > 0 ? 'green' : 'red'}
          opacity={'0.2'}
        />
        <line
          x1={x(1)}
          x2={x(1) + getLineLength(vecDist1[i])}
          y1={y($predictions[1][i])}
          y2={y($predictions[1][i])}
          fill="none"
          stroke={vecDist1[i] > 0 ? 'green' : 'red'}
          opacity={'0.2'}
        />
      {/each}
    </g>

    <!-- x axis -->
    <g transform="translate(0,{height - margin.bottom})">
      {#each ['Model 1', 'Model 2'] as tick, i}
        <g transform="translate({x(i)})">
          <line y1={0} y2={tickSize} stroke="black" />
          <text
            y={tickSize + 2}
            text-anchor="middle"
            dominant-baseline="hanging"
            font-size="12"
            fill="black"
          >
            {tick}
          </text>
        </g>
      {/each}
    </g>

    <!-- y axis -->
    <g class="axis" id="model1-axis" transform="translate({margin.left})">
      {#each y.ticks() as tick}
        <g transform="translate(0,{y(tick)})">
          <line x1={0} x2={-tickSize} stroke="black" />
          <text
            x={-tickSize - 2}
            text-anchor="end"
            dominant-baseline="middle"
            font-size="12"
            fill="black"
          >
            {tick}
          </text>
        </g>
      {/each}
    </g>
    <g
      class="axis"
      id="model2-axis"
      transform="translate({width - margin.right})"
    >
      {#each y.ticks() as tick}
        <g transform="translate(0,{y(tick)})">
          <line x1={0} x2={tickSize} stroke="black" />
          <text
            x={tickSize + 2}
            text-anchor="start"
            dominant-baseline="middle"
            font-size="12"
            fill="black"
          >
            {tick}
          </text>
        </g>
      {/each}
    </g>
  </g>
</svg>

<style>
</style>
