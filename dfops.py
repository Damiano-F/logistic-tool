import pandas as pd

# sums selected rows and columns, returns modified dataframe
def cluster_sum(matrix, cluster):

    i = 2
    while i>0:
        matrix[tuple(cluster)] = matrix[cluster].sum(axis=1)
        matrix = matrix.drop(cluster, axis=1)
        matrix = matrix.T
        i = i - 1

    return matrix

# sums values of row (j) and column (i) indexes, avoiding to count center cross 2 times
def cross_sum(matrix, i, j, cross):

    col_sum = matrix[i].drop(j).sum()
    matrix = matrix.T
    row_sum = matrix[j].drop(i).sum()

    if cross == True:
        cross_center = matrix.at[j, i]
        cross_sum = col_sum + row_sum + cross_center
    else:
        cross_sum = col_sum + row_sum

    return cross_sum