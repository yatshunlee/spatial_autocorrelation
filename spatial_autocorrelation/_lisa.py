import numpy as np
import pandas as pd

def cal_EXP_Ii(wi, n):
    return (-wi) / (n - 1)

def cal_b2i(N, D_power_of_4, D_sq, D, i):
    numerator = N * (np.sum(D_power_of_4) - D[i])
    denominator = (np.sum(D_sq) - D_sq[i]) ** 2
    return numerator / denominator

def local_moransI(w_mat, y, y_name):
    # cal para
    y_hat = np.mean(y)
    N = y.shape[0]
    W = np.copy(w_mat).astype('float')

    D = y - y_hat
    D_sq = (y - y_hat) ** 2
    D_power_of_4 = [d ** 4 for d in D]

    # calculating the LISA of each y value
    lisa = []

    for i in range(N):
        tmp_I = 0
        for j in range(N):
            tmp_I += W[i, j] * D[j]
        tmp_I *= (N * D[i] / np.sum(D_sq))

        lisa.append(tmp_I)

    lisa = np.array(lisa).reshape(-1, 1)

    # Expected value of each local Moran's I
    EXP_Ii = []

    for i in range(N):
        EXP_Ii.append(cal_EXP_Ii(np.sum(W[i, :]), N))

    # calculating the variance of each local Moran's I
    b2i = []

    for i in range(N):
        b2i.append(cal_b2i(N, D_power_of_4, D_sq, D, i))

    VAR_Ii = []

    for i in range(N):
        var = (N - b2i[i]) * 1 ** 2 / (N - 1) - (
                    (2 * b2i[i] - N) * np.sum(np.multiply(W[i, :], W[i, :])) / ((N - 1) * (N - 2))) - EXP_Ii[i] ** 2
        VAR_Ii.append(var)

    # integrate the result as a dataframe
    Ii_results = pd.DataFrame({
        'Name':y_name, 
        'LISA':list(lisa.reshape(-1)), 
        'E(Ii)':EXP_Ii, 
        'VAR(Ii)':VAR_Ii
    })
    Ii_results['Z Score'] = [
        (Ii_results.loc[i, 'LISA'] - Ii_results.loc[i, 'E(Ii)']) / Ii_results.loc[i, 'VAR(Ii)'] ** 0.5
        for i in range(Ii_results.shape[0])
    ]

    return Ii_results
