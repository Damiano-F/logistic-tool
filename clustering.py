from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pandas as pd

X = np.array([[1, 2], [1, 4], [1, 0],
              [4, 2], [4, 4], [4, 0]])
clustering = AgglomerativeClustering().fit(X)

sim_dict = {'a': {'a': 1, 'b': 0.5, 'c': 0},
            'b': {'a': 0.5, 'b': 1, 'c': 0},
            'c': {'a': 0.5, 'b': 0, 'c': 1}}

sim_matrix = pd.DataFrame.from_dict(sim_dict)

clust = AgglomerativeClustering(n_clusters=2, affinity='cosine', linkage='average').fit_predict(sim_matrix)

def clusters(sim, link_name):

    clusters_num = len(sim.columns) - 1

    clusters_collection = []
    while clusters_num >= 1:
        clusters = AgglomerativeClustering(n_clusters=clusters_num, affinity='cosine', linkage=link_name).fit_predict(sim)
        clusters_collection.append(clusters)
        clusters_num = clusters_num - 1

    return clusters_collection

sim_matrix = pd.read_excel(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\Es sim asimmetrica\sim asimmetrica.xlsx')
sim_matrix.index = sim_matrix.columns
print(sim_matrix)

print(clusters(sim_matrix, 'average'))