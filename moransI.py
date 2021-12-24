import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Formula is from:
# link: https://en.wikipedia.org/wiki/Moran%27s_I

def get_moransI(ori_w, y):
    # w = spatial weight (topological or actual distance)
    # y = actual value
    # y_hat = mean value
    
    if not isinstance(y, np.ndarray):
        raise TypeError("Passed array (feature) should be in numpy array (ndim = 1)")
    if y.shape[0] != ori_w.shape[0]:
        raise ValueError("Feature array is not the same shape of weight")
    if ori_w.shape[0] != ori_w.shape[1]:
        raise ValueError("Weight array should be in square shape")
    
    w = np.copy(ori_w).astype('float')
    
    y_hat = np.mean(y)
    D = y - y_hat
    D_sq = (y - y_hat)**2
    
    N = y.shape[0]
    
    # ΣiΣj wij
    sum_W = np.sum(w)

    # W x D:
    # Wij x (Yi-Y_hat) x (Yj-Y_hat)
    for i in range(N):
        for j in range(N):
            if w[i,j]!=0:
                w[i,j]*=D[i]*D[j]

    moransI = (np.sum(w)/sum(D_sq)) * (N / sum_W)
    
    return round(moransI,8)
    

def get_expected_moransI(y):
    N = y.shape[0]
    EXP_I = -1 / (N-1)
    return EXP_I
    

def get_var_moransI(ori_w, y, EXP_I):

    if not isinstance(y, np.ndarray):
        raise TypeError("Passed array (feature) should be in numpy array (ndim = 1)")
    if y.shape[0] != ori_w.shape[0]:
        raise ValueError("Feature array is not the same shape of weight")
    if ori_w.shape[0] != ori_w.shape[1]:
        raise ValueError("Weight array should be in square shape")

    y_hat = np.mean(y)
    D = y - y_hat
    D_sq = (y - y_hat)**2

    N = y.shape[0]

    # use the original weights
    w = np.copy(ori_w).astype('float')
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


def hypothesis_testing(moransI, ori_w, y):
    # The null hypothesis for the test is that the data is randomly disbursed.
    # The alternate hypothesis is that the data is more spatially clustered than you would expect by chance alone.
    # Two possible scenarios are:
    # 1) A positive z-value: data is spatially clustered in some way.
    # 2) A negative z-value: data is clustered in a competitive way.
    #    For example, high values may be repelling high values or negative values may be repelling negative values.
    EXP_moransI = get_expected_moransI(y)
    VAR_moransI = get_var_moransI(ori_w, y, EXP_moransI)

    print('The expected value of Moran\'s I:', EXP_moransI)
    print('The variance of Moran\'s I:', VAR_moransI)
    print('Z score of Moran\'s I:', (moransI - EXP_moransI) / VAR_moransI ** 0.5)


def normalize_y(ori_w, y):
    W_Y = np.copy(ori_w)

    i, j = np.where(W_Y > 0)

    first = True
    lst = []
    avg_list = []

    for k in range(len(i)):
        if not first and i_idx != i[k]:
            avg_list.append(np.mean(lst))
            lst = []

        first = False

        i_idx, j_idx = i[k], j[k]

        lst.append(y[j_idx])

    avg_list.append(np.mean(lst))

    if not isinstance(y, np.ndarray):
        normalized_y = [(ele - np.mean(y.values)) / np.std(y.values) for ele in y.values]
    else:
        normalized_y = [(ele - np.mean(y)) / np.std(y) for ele in y]
    normalized_avg_list = [(ele - np.mean(avg_list)) / np.std(avg_list) for ele in avg_list]

    # transform into numpy array
    normalized_y = np.array(normalized_y)
    normalized_avg_list = np.array(normalized_avg_list)
    return normalized_y, normalized_avg_list


def moransI_scatterplot(moransI, ori_w, y):
    normalized_y, normalized_avg_list = normalize_y(ori_w, y)

    # HH
    hh_idx = np.intersect1d(np.where((np.array(normalized_y) > 0)), np.where((np.array(normalized_avg_list) > 0)))
    # low values surrounded by high values (outliers)
    lh_idx = np.intersect1d(np.where((np.array(normalized_y) <= 0)), np.where((np.array(normalized_avg_list) > 0)))
    # high values surrounded by low values (outliers)
    hl_idx = np.intersect1d(np.where((np.array(normalized_y) > 0)), np.where((np.array(normalized_avg_list) <= 0)))
    # LL
    ll_idx = np.intersect1d(np.where((np.array(normalized_y) <= 0)), np.where((np.array(normalized_avg_list) <= 0)))

    # plot different regions: High-High, High-Low, Low-High, Low-Low
    plt.scatter(normalized_y[hh_idx], normalized_avg_list[hh_idx],
                color='blue', alpha=0.5)
    plt.scatter(normalized_y[lh_idx], normalized_avg_list[lh_idx],
                color='blue', alpha=0.5)
    plt.scatter(normalized_y[hl_idx], normalized_avg_list[hl_idx],
                color='blue', alpha=0.5)
    plt.scatter(normalized_y[ll_idx], normalized_avg_list[ll_idx],
                color='blue', alpha=0.5)

    # separate the graph into 4 quartiles
    plt.axvline(x=0, linestyle='--', color='k', alpha=0.5)
    plt.axhline(y=0, linestyle='--', color='k', alpha=0.5)

    # plot moran's I
    x = np.linspace(-5, 5, 100)
    plt.plot(x, moransI * x, color='red')

    # layout
    plt.title(f'Moran\'s I: {moransI:.4f}')
    plt.xlabel('y')
    plt.ylabel('Lagged y')


def cal_EXP_Ii(wi, n):
    return (-wi) / (n - 1)


def cal_b2i(N, D_power_of_4, D_sq, D, i):
    numerator = N * (np.sum(D_power_of_4) - D[i])
    denominator = (np.sum(D_sq) - D_sq[i]) ** 2
    return numerator / denominator


def get_localMoransI(ori_w, y, y_name):
    # cal para
    y_hat = np.mean(y)
    N = y.shape[0]
    W = np.copy(ori_w).astype('float')

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
    Ii_results = {'Name':y_name, 'LISA':list(lisa.reshape(-1)), 'E(Ii)':EXP_Ii, 'VAR(Ii)':VAR_Ii}
    Ii_results = pd.DataFrame(Ii_results)
    Ii_results['Z Score'] = [
        (Ii_results.loc[i, 'LISA'] - Ii_results.loc[i, 'E(Ii)']) / Ii_results.loc[i, 'VAR(Ii)'] ** 0.5
        for i in range(Ii_results.shape[0])]

    return Ii_results


def LISA_scatterplot(moransI, ori_w, y, Ii_results):
    normalized_y, normalized_avg_list = normalize_y(ori_w, y)

    high_high = Ii_results[(abs(Ii_results['Z Score']) >= 2)].loc[Ii_results.LISA > 0].index
    insignificant = Ii_results[(abs(Ii_results['Z Score']) <= 2)].index
    low_low = Ii_results[(abs(Ii_results['Z Score']) >= 2)].loc[Ii_results.LISA < 0].index

    # plot different regions: High-High, Insignificant, Low-Low
    plt.scatter(normalized_y[high_high], normalized_avg_list[high_high],
                color='red', alpha=0.5)
    plt.scatter(normalized_y[insignificant], normalized_avg_list[insignificant],
                color='gray', alpha=0.2)
    plt.scatter(normalized_y[low_low], normalized_avg_list[low_low],
                color='blue', alpha=0.5)

    # separate the graph into 4 quartiles
    plt.axvline(x=0, linestyle='--', color='k', alpha=0.5)
    plt.axhline(y=0, linestyle='--', color='k', alpha=0.5)

    # plot moran's I
    x = np.linspace(-5, 20, 100)
    plt.plot(x, moransI * x, color='red')

    # layout
    plt.title(f'Moran\'s I: {moransI:.4f}')
    plt.xlabel('Views')
    plt.ylabel('W_Views')