import { range } from 'd3-array';
//import { groundTruth, minDiffFromTruth, model1BrushedExtent, model2BrushedExtent, predictions } from './stores';
export {getFilteredIndices};


function getFilteredIndices(size: number, minPredictionDifference: number, model1BrushedExtent: [number, number], model2BrushedExtent: [number, number], minDiffFromTruth: number, gt: number[], predictions: [number[], number[]]): number[] {
    return range(size).filter(i => {
        return Math.abs(predictions[0][i] - predictions[1][i]) >= minPredictionDifference
        && Math.abs(predictions[0][i] - gt[i]) >= minDiffFromTruth && Math.abs(predictions[1][i] - gt[i]) >= minDiffFromTruth
        && predictions[0][i] >= model1BrushedExtent[0] && predictions[0][i] <= model1BrushedExtent[1]
        && predictions[1][i] >= model2BrushedExtent[0] && predictions[1][i] <= model2BrushedExtent[1] ;
    })
}
