import numpy as np
import scipy.sparse
import shap
import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)
warnings.DeprecationWarning = DeprecationWarning


def getPredictions(stdmodel1, stdmodel2, stdX_test):
    print("Start...")
    #stdX_csr = scipy.sparse.csr_matrix(list(stdX_test.values()))
    print("Predictions obtained")
    return [stdmodel1(stdX_test), stdmodel2(stdX_test)]

def calculateShaps(stdmodel1, stdmodel2, stdX_test):
    # this is not a NN
    print("Shaps now")
    print("Shaps XGB")
    expl1 = shap.Explainer(stdmodel1, stdX_test)
    # this is a NN
    print("Shaps NN")
    expl2 = shap.Explainer(stdmodel2, stdX_test)
    # calculating shap
    print("Calculating...")
    print("-> xgb")
    shap1 = expl1(stdX_test)
    print("-> nn")
    shap2 = expl2(stdX_test)
    print("Difference...")
    shapD = shap1 - shap2
    print("Done")
    shap1_array = np.array(shap1.values)
    shap2_array = np.array(shap2.values)
    shapD_array = shap1_array - shap2_array
    return shap1_array.tolist(), shap2_array.tolist(), shapD_array.tolist()
