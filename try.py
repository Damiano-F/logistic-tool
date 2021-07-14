import pandas as pd
from dfops import cross_sum, cluster_sum

from_to = pd.read_excel(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\Es layout\layout_sample.xlsx')
from_to = from_to.set_axis(from_to.columns, axis='index')
print('Original From-To:')
print(from_to)

print('Row Index and Cross Sum')
print(cross_sum(from_to, 'm1', 'm1', False))

from_to = cluster_sum(from_to, ['m1', 'm2'])
print('Cluster Sum')
print(from_to)

#print('Row Index and Cross Sum')
#print(cross_sum(from_to, ['m1', 'm2'], ['m1', 'm2'], False))