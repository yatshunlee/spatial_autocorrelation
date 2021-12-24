# spatial_autocorrelation
Performing Moran's I to conduct correlation analysis on topological/geometrical relationship.

Moran's I, developed by Patrick Alfred Pierce Moran [1], measures spatial autocorrelation globally based on the feature locations and values. It quantifies the relationship how clustered the values of data points geometrically are, i.e. the spatial lagged.

# Requirements
This module is expected to compile for 'python 3.7-3.9'

# Usage
You have to customly define the spatial weighted matrix for describing the topogical/geometrical relationship.
You may want to refer to example/Spatial Autocorrelation.ipynb.

## For Moran's I (global metric)
Moran's I is within-1 and 1.
- -1 represents perfectly dispersed
- 0 represents randomness
- 1 represents perfectly clustered

For calculating the global Moran's I, you can execute

    from spatial_autocorrelation import global_moransI
    
You are also able to visualize the global relationship on a plot

    from spatial_autocorrelation import moransI_scatterplot
    
Since it is a inferential statistics, the Moran's I value can be converted into Z score for conducting statistical hypothesis testing

    from spatial_autocorrelation import hypothesis_testing

## For LISA (local metric)
You can retrieve a dataframe containing local Moran's I, Z score of each individual data point by using

    from spatial_autocorrelation import get_localMoransI
    
You can also visualize the high-high, high-low, low-high, low-low clusters on a plot

    from spatial_autocorrelation import LISA_scatterplot
    
References:
1) https://en.wikipedia.org/wiki/Moran%27s_I
2) https://www.statology.org/morans-i/
3) https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-statistics/h-how-spatial-autocorrelation-moran-s-i-spatial-st.htm
4) http://ceadserv1.nku.edu/longa//geomed/ppa/doc/LocalI/LocalI.htm
