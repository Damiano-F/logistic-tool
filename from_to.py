import math
import pandas as pd
from dfops import cluster_sum

def from_to(vehicles, demands, visits, workshops, clusters, bom):

    pallets_day = {}
    for v in vehicles:
        pallets_per_vehicle = {}
        for p in v.capacity:
            if v.capacity.at[0, p] != 0:
                pallets = math.ceil(demands[p] / v.capacity.at[0, p])
            else:
                pallets = 0
            pallets_per_vehicle.update({p: pallets})
        pallets_day.update({v.name: pallets_per_vehicle})

    total_pallets = dict(zip(demands.keys(), [0]*len(demands)))
    for v in pallets_day:
        for p in pallets_day[v]:
            total_pallets.update({p: total_pallets[p] + pallets_day[v][p]})

    from_to_list = []
    from_to = pd.DataFrame(index=workshops, columns=workshops).fillna(0)
    from_to_list.append(from_to)

    for p in visits:
        for el, el2 in zip(visits[p], visits[p][1:]):
            if el[0] == el2[0]:
                pass
            else:
                from_to.at[el[0], el2[0]] = from_to.at[el[0], el2[0]] + total_pallets[p]

    for p in bom.columns:
        for p2 in bom.index:
            if bom.at[p2, p] != 0:
                bom.at[p2, p] = bom.at[p2, p] * demands[p]

    for v in vehicles:
        for p in bom.columns:
            for p2 in bom.index:
                if bom.at[p2, p] != 0 and v.capacity.at[0, p2] != 0:
                    bom.at[p2, p] = math.ceil(bom.at[p2, p] / v.capacity.at[0, p2])

    for p in bom.index:
        for p2 in bom.columns:
            if bom.at[p, p2] > 0:
                row = visits[p][-1][0]
                col = visits[p2][0][0]
                from_to.at[row, col] = from_to.at[row, col] + bom.at[p, p2]

    for el in clusters:
        clusters_from_to = pd.DataFrame(index=workshops, columns=workshops)
        for ws in workshops:
            for ws2 in workshops:
                clusters_from_to.at[ws, ws2] = from_to.at[ws, ws2]
        for c in el.values():
            if type(c) == list:
                clusters_from_to = cluster_sum(clusters_from_to, c)
        from_to_list.append(clusters_from_to)

    return from_to_list