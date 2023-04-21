import numpy as np

def getPredictions(model1, model2, df):
    return [model1(df), model2(df)]

def calculateShaps(model1, model2, df):
    shap1 = np.random.rand(df.shape[0],df.shape[1]) -0.5
    shap2 = np.random.rand(df.shape[0],df.shape[1]) -0.5
    shapD = shap1 - shap2
    return shap1.tolist(), shap2.tolist(), shapD.tolist()
