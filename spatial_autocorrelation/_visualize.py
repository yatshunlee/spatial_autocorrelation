import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def normalize_y(w_mat, y):
    W_Y = np.copy(w_mat)

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

def moransI_scatterplot(moransI, w_mat, y):
    normalized_y, normalized_avg_list = normalize_y(w_mat, y)

    # HH
    hh_idx = np.intersect1d(np.where((np.array(normalized_y) > 0)),
                            np.where((np.array(normalized_avg_list) > 0)))
    # low values surrounded by high values (outliers)
    lh_idx = np.intersect1d(np.where((np.array(normalized_y) <= 0)),
                            np.where((np.array(normalized_avg_list) > 0)))
    # high values surrounded by low values (outliers)
    hl_idx = np.intersect1d(np.where((np.array(normalized_y) > 0)),
                            np.where((np.array(normalized_avg_list) <= 0)))
    # LL
    ll_idx = np.intersect1d(np.where((np.array(normalized_y) <= 0)),
                            np.where((np.array(normalized_avg_list) <= 0)))
    
    plt.figure(figsize=(8, 6))
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
    x_min = np.min(normalized_y) - 3
    x_max = np.max(normalized_y) + 3
    x = np.linspace(x_min, x_max, 100)
    plt.plot(x, moransI * x, color='red')

    # layout
    plt.title(f'Moran\'s I: {moransI:.4f}')
    plt.xlabel('y')
    plt.ylabel('Lagged y')
    
    plt.show()
    
def LISA_scatterplot(moransI, w_mat, y, Ii_results):
    normalized_y, normalized_avg_list = normalize_y(w_mat, y)
    
    plt.figure(figsize=(8, 6))
    
    # plot different regions: High-High, Insignificant, Low-Low
    high_high = Ii_results[(abs(Ii_results['Z Score']) >= 2)].loc[Ii_results.LISA > 0].index
    plt.scatter(normalized_y[high_high],
                normalized_avg_list[high_high],
                color='red', alpha=0.5)
    
    insignificant = Ii_results[(abs(Ii_results['Z Score']) <= 2)].index
    plt.scatter(normalized_y[insignificant],
                normalized_avg_list[insignificant],
                color='gray', alpha=0.2)
    
    low_low = Ii_results[(abs(Ii_results['Z Score']) >= 2)].loc[Ii_results.LISA < 0].index
    plt.scatter(normalized_y[low_low],
                normalized_avg_list[low_low],
                color='blue', alpha=0.5)

    # separate the graph into 4 quartiles
    plt.axvline(x=0, linestyle='--', color='k', alpha=0.5)
    plt.axhline(y=0, linestyle='--', color='k', alpha=0.5)

    # plot moran's I
    x_min = np.min(normalized_y) - 3
    x_max = np.max(normalized_y) + 3
    x = np.linspace(x_min, x_max, 100)
    plt.plot(x, moransI * x, color='red')

    # layout
    plt.title(f'Moran\'s I: {moransI:.4f}')
    plt.xlabel('Views')
    plt.ylabel('W_Views')
    
    plt.show()