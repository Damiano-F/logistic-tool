from dictops import maximum_keys
import pandas as pd
from loader import Loader
from plant import Plant

loader_ = Loader(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\cycles_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\demand_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\bom_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\workshops_sample.xlsx')

plant = Plant(loader_)

sim = plant.gupt_seiff
clusters = [ws for ws in sim.index]

def grouping(sim, clusters):

    # sim matrix copy
    sim2 = pd.DataFrame(index=sim.index, columns=sim.columns)
    for row in sim.index:
        for col in sim.columns:
            sim2.at[row, col] = sim.at[row, col]

    # determines next clustering
    compare = 0
    max_dict = {}
    for row in sim2.index:
        for col in sim2.columns:
            if row == col:
                pass
            else:
                if compare <= sim2.at[row, col]:
                    max_dict.update({(row, col): sim2.at[row, col]})
    max_vals = maximum_keys(max_dict)
    cluster = max_vals[0][0]

    # sets new matrix indexes (current clusters)
    clusters.append(cluster)
    for ws in sim.columns:
        if ws in cluster:
            clusters.remove(ws)

    #sets new indexes
    indexes = []
    for el in clusters:
        if type(el) == tuple:
            index = el[0]+el[1]
            indexes.append(index)
        else:
            indexes.append(el)

    # sets modified sim matrix
    sim2 = pd.DataFrame(index=indexes, columns=indexes)
    print(sim2)
    for row in sim2.index:
        for col in sim2.columns:
            if row == col:
                sim2.at[row, col] = 1
            else:
                den = len(row) * len(col)
                num = 0
                for el in row:
                    for el2 in col:
                        num = num + sim.at[el, el2]
                sim2.at[row, col] = num/den


    """
    # return
    if len(sim2.index) == 1:
        return clusters
    else:
        grouping(sim2, clusters)"""

grouping(sim, clusters)