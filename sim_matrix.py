import pandas as pd
import numpy as np
import math

def sim_init(ws_list):

    # df creation
    sim_init = pd.DataFrame(index=ws_list, columns=ws_list)

    # diagonal filling
    np.fill_diagonal(sim_init.values, 1)
    
    return sim_init

def symm_df(data_frame):

    for x in data_frame.index:
        for y in data_frame.columns:
            if data_frame.at[x, y] == data_frame.at[y, x]:
                return True
            else:
                return False

def baroni_urbani(ws_list, pmim):

    sim_matrix = sim_init(ws_list)

    for ws in pmim.index:
        for ws2 in pmim.index:
            if ws != ws2:
                a, b, c, d = 0, 0, 0, 0
                for part in pmim.columns:
                    if pmim.at[ws, part] == 0 and pmim.at[ws2, part] == 1:
                        b = b + 1
                    elif pmim.at[ws, part] == 1 and pmim.at[ws2, part] == 0:
                        c = c + 1
                    elif pmim.at[ws, part] == 0 and pmim.at[ws2, part] == 0:
                        d = d + 1 - pmim.at[ws, part] + pmim.at[ws2, part]
                    elif pmim.at[ws, part] == 1 and pmim.at[ws2, part] == 1:
                        a = a + 1
                sim_matrix.at[ws, ws2] = (a + math.sqrt(a * d)) / (a + b + c + math.sqrt(a * d))

    # symmetrism check
    if symm_df(sim_matrix) == False:
        raise Exception('similarity matrix not symmetric')

    return sim_matrix

def gupta_seiffodini(ws_list, pmim, visits, demands):

    sim_matrix = sim_init(ws_list)

    # sintetic version of visits
    sint_visits = {}
    for part in visits:
        sint_phases = []
        for phase in visits[part]:
            sint_phases.append([visits[part][phase]['w'], visits[part][phase]['t']])
        sint_visits.update({part: sint_phases})

    for ws in sim_matrix.index:
        for ws2 in sim_matrix.columns:
            if ws != ws2:
                num = 0
                den = 0
                for part in pmim:
                    t = 0
                    z = 0
                    x = pmim.at[ws, part] * pmim.at[ws2, part]
                    y = 0
                    if x == 0:
                        y = pmim.at[ws, part] + pmim.at[ws2, part]
                    if x == 1:
                        t0 = 0
                        t1 = 0
                        for el in sint_visits[part]:
                            if ws == el[0]:
                                t0 = t0 + el[1]
                            if ws2 == el[0]:
                                t1 = t1 + el[1]
                        t = min(t0, t1) / max(t0, t1)
                        for el, el2 in zip(sint_visits[part], sint_visits[part][1:]):
                            if (el[0] and el2[0]) in [ws, ws2]:
                                z = z + 1
                    xxt = x * t
                    num = num + (xxt + z) * demands[part]
                    den = den + (xxt + z + y) * demands[part]
                sim_matrix.at[ws, ws2] = num / den

    # symmetrism check
    if symm_df(sim_matrix) == False:
        raise Exception('similarity matrix not symmetric')

    return sim_matrix

