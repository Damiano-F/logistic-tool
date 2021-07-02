from sklearn.cluster import AgglomerativeClustering
from dictops import append_value

def clusters(sim, link_type):

    clusters_num = len(sim.columns) - 1

    clusters_collection = []
    while clusters_num >= 2:
        clusters = AgglomerativeClustering(n_clusters=clusters_num, affinity='cosine', linkage=link_type).fit(sim)
        clusters_collection.append(clusters.labels_)
        clusters_num = clusters_num - 1

    clusters_dicts = []
    for el in clusters_collection:
        clusters_dict = {}
        for i in range(len(sim.columns)):
            append_value(clusters_dict, el[i], sim.columns[i])
        clusters_dicts.append(clusters_dict)

    return clusters_dicts


# test for clusters
# sim_matrix = pd.read_excel(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\Es sim asimmetrica\sim asimmetrica.xlsx')
# sim_matrix.index = sim_matrix.columns
# print(sim_matrix)

# print(clusters(sim_matrix, 'average'))
