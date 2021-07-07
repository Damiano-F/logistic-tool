import pandas as pd

# sums selected rows and columns, returns modified dataframe
def cluster_sum(matrix, cluster):

    matrix[tuple(cluster)] = matrix[cluster].sum(axis=1)
    matrix = matrix.drop(cluster, axis=1)
    matrix = matrix.append(pd.Series(matrix.loc[cluster, :].sum(axis=0), name=tuple(cluster)))
    matrix = matrix.drop(cluster, axis=0)

    return matrix

# sums values of row (j) and column (i) indexes, avoiding to count center cross 2 times
def cross_sum(matrix, i, j):

    cross_center = matrix.at[j, i]
    col_sum = matrix[i].drop(j).sum()
    row_sum = matrix.loc[j, :].drop(i).sum()

    cross_sum = col_sum + row_sum + cross_center

    return cross_sum