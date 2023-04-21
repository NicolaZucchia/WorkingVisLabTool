import { range } from 'd3-array';
export {getFilteredIndices};

function getFilteredIndices(size: number, minPredictionDifference: number, model1BrushedExtent: [number, number], model2BrushedExtent: [number, number], predictions: [number[], number[]]): number[] {
    return range(size).filter(i => {
        return Math.abs(predictions[0][i] - predictions[1][i]) >= minPredictionDifference
        && predictions[0][i] >= model1BrushedExtent[0] && predictions[0][i] <= model1BrushedExtent[1]
        && predictions[1][i] >= model2BrushedExtent[0] && predictions[1][i] <= model2BrushedExtent[1] ;
    })
}