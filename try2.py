import pandas as pd
import numpy as np

def cluster_sum(matrix, cluster):

    matrix[tuple(cluster)] = matrix[cluster].sum(axis=1)
    matrix = matrix.drop(cluster, axis=1)
    matrix = matrix.T
    matrix[tuple(cluster)] = matrix[cluster].sum(axis=1)
    matrix = matrix.drop(cluster, axis=1)
    matrix = matrix.T

    return matrix

idx = ['a', 'b', 'c']
matrix = pd.DataFrame(np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]]), index=idx, columns=idx)
print(matrix)

cluster = ['a', 'b']

new_matrix = cluster_sum(matrix, cluster)
print(new_matrix)

new_matrix2 = cluster_sum(new_matrix, ['c', ('a', 'b')])
print(new_matrix2)