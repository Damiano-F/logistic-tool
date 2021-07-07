import pandas as pd

from_to = pd.read_excel(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\Es layout\layout_sample.xlsx')
from_to = from_to.set_axis(from_to.columns, axis='index')
print(from_to)

def cross_sum(matrix, i, j):

    cross_center = matrix.at[j, i]
    col_sum = matrix[i].drop(j).sum()
    row_sum = matrix.loc[j, :].drop(i).sum()

    cross_sum = col_sum + row_sum + cross_center

    return cross_sum

print(cross_sum(from_to, 'm1', 'm2'))