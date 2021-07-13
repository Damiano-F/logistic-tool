import pandas as pd

# sums selected rows and columns, returns modified dataframe
def cluster_sum(matrix, cluster):

    matrix[tuple(cluster)] = matrix[cluster].sum(axis=1)
    matrix = matrix.drop(cluster, axis=1)
    matrix = matrix.append(pd.Series(matrix.loc[cluster, :].sum(axis=0), name=tuple(cluster)))
    matrix = matrix.drop(cluster, axis=0)

    return matrix

# sums values of row (j) and column (i) indexes, avoiding to count center cross 2 times
def cross_sum(matrix, i, j, cross):

    col_sum = matrix[i].sum() - matrix.at[j, i]
    row_sum = matrix.loc[j, :].sum() - matrix.at[j, i]

    if cross == True:
        cross_center = matrix.at[j, i]
        cross_sum = col_sum + row_sum + cross_center
    else:
        cross_sum = col_sum + row_sum

    return cross_sum