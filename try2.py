import pandas as pd
from loader import Loader
from plant import Plant
from tupleops import  flatten
from dictops import max_nested, remove_as_df


loader_ = Loader(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\cycles_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\demand_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\bom_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\workshops_sample.xlsx')

plant = Plant(loader_)

sim = plant.gupt_seiff
sim_dict = sim.to_dict()

clusters = [ws for ws in sim_dict]
print(clusters)

def grouping(sim, clusters):

    # determines next clustering
    max_values = max_nested(sim)
    cluster = max_values[0][0]

    for ws in cluster:
        sim = remove_as_df(sim, ws)

    print(sim)



grouping(sim_dict, clusters)