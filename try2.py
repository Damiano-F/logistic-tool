import pandas as pd
import numpy as np

def cluster_sum(matrix, cluster):

    matrix[tuple(cluster)] = matrix[cluster].sum(axis=1)
    matrix = matrix.drop(cluster, axis=1)
    matrix = matrix.append(pd.Series(matrix.loc[cluster, :].sum(axis=0), name=tuple(cluster)))
    matrix = matrix.drop(cluster, axis=0)

    return matrix

idx = ['a', 'b', 'c']
sample_df = pd.DataFrame(np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]]), index=idx, columns=idx)
print(sample_df)

cluster = ['a', 'b']

new_df = cluster_sum(sample_df, cluster)
print(new_df)

print(new_df[('a', 'b')])
print(new_df.loc[('a', 'b'), :])