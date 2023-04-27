import numpy as np
import scipy.sparse
import shap
import warnings
import math
warnings.simplefilter("ignore", category=DeprecationWarning)
warnings.DeprecationWarning = DeprecationWarning

def shapAbsSumCalc(shapInstance):
    tmp_sum = 0
    for i in shapInstance:
        tmp_sum += abs(i)
    return tmp_sum

def typeTransformer(current_shaps):
    tmp_list = []
    for i in range(0, len(current_shaps)):
        tmp_dict = {
            "instance": i,
            "shap": current_shaps[i],
            "shapAbsSum": shapAbsSumCalc(current_shaps[i])
        }
        tmp_list.append(tmp_dict)
    return tmp_list

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
    print("-> m1")
    shap1 = expl1(stdX_test)
    print("-> m2")
    shap2 = expl2(stdX_test)
    print("Difference...")
    shapD = shap1 - shap2
    print("Done")
    shap1_array = np.array(shap1.values)
    shap2_array = np.array(shap2.values)
    shapD_array = shap1_array - shap2_array
    return typeTransformer(shap1_array), typeTransformer(shap2_array), typeTransformer(shapD_array)
