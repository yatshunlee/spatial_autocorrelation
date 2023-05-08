import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Formula is from:
# link: https://en.wikipedia.org/wiki/Moran%27s_I

def get_expected_moransI(y):
    N = y.shape[0]
    EXP_I = -1 / (N-1)
    return EXP_I
    

def get_var_moransI(w_mat, y, EXP_I):

    if not isinstance(y, np.ndarray):
        raise TypeError("Passed array (feature) should be in numpy array (ndim = 1)")
    if y.shape[0] != w_mat.shape[0]:
        raise ValueError("Feature array is not the same shape of weight")
    if w_mat.shape[0] != w_mat.shape[1]:
        raise ValueError("Weight array should be in square shape")

    y_hat = np.mean(y)
    D = y - y_hat
    D_sq = (y - y_hat)**2

    N = y.shape[0]

    # use the original weights
    w = np.copy(w_mat).astype('float')
    sum_W = np.sum(w)

    # Calculating S1
    S1 = 0

    for i in range(N):
        for j in range(N):
            S1 += (w[i,j]+w[j,i])**2
            
    S1 *= 0.5

    # Calculating S2
    S2 = 0

    for i in range(N):
        sum_wij, sum_wji = 0, 0
        
        for j in range(N):
            sum_wij += w[i,j]
        for j in range(N):
            sum_wji += w[j,i]
        
        S2 += (sum_wij + sum_wji)**2
        
    # Calculating S3 
    D_power_of_4 = [d**4 for d in D]

    S3 = (1/N * sum(D_power_of_4)) / (1/N * sum(D_sq))**2

    # Calculating S4
    S4 = (N**2 - 3*N + 3) * S1 - N * S2 + 3 * sum_W**2

    # Calculating S5
    S5 = (N**2 - N) * S1 - 2 * N * S2 + 6 * sum_W**2
    
    VAR_I = (N * S4 - S3 * S5) / ((N-1) * (N-2) * (N-3) * sum_W**2) - EXP_I**2
    
    return VAR_I


def hypothesis_testing(moransI, w_mat, y):
    # The null hypothesis for the test is that the data is randomly disbursed.
    # The alternate hypothesis is that the data is more spatially clustered than you would expect by chance alone.
    # Two possible scenarios are:
    # 1) A positive z-value: data is spatially clustered in some way.
    # 2) A negative z-value: data is clustered in a competitive way.
    #    For example, high values may be repelling high values or negative values may be repelling negative values.
    EXP_moransI = get_expected_moransI(y)
    VAR_moransI = get_var_moransI(w_mat, y, EXP_moransI)

    print('The expected value of Moran\'s I:', EXP_moransI)
    print('The variance of Moran\'s I:', VAR_moransI)
    print('Z score of Moran\'s I:', (moransI - EXP_moransI) / VAR_moransI ** 0.5)