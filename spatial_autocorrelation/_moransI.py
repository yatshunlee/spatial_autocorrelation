import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def moransI(w, y):
    '''
    :param: w_mat (array-like): spatial weight sqaure matrix (can be topogical or any distance)
    :parm: y (array-like): feature array
    '''
    if not isinstance(y, np.ndarray):
        raise TypeError("Passed array (feature) should be in numpy array (ndim = 1)")
    if y.shape[0] != w_mat.shape[0]:
        raise ValueError("Feature array is not the same shape of weight")
    if w_mat.shape[0] != w_mat.shape[1]:
        raise ValueError("Weight array should be in square shape")
    
    w = w.astype('float')
    
    y_hat = np.mean(y)
    D = y - y_hat
    D_sq = (y - y_hat)**2
    
    N = y.shape[0]

    moransI = (D @ w @ D / np.sum(D_sq)) * (N / np.sum(w))
    
    return moransI