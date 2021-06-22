import math
import pandas as pd
from dictops import nestdict, ddict2dict, maximum_keys

class Plant:

    def __init__(self, loader):

        self.loader = loader
        self.workshops = self.loader.get_workshops()
        self.visits = self.loader.get_visits()
        self.demands = self.loader.get_demands()

        self.pmim = 'undefined'
        self.baroni_urbani = 'undefined'
        self.gupt_seiff = 'undefined'
        self.clusters = []

        # sets automation level
        for workshop in self.workshops:
            workshop.set_automation()

        # computes disposable times
        for workshop in self.workshops:
            workshop.set_disp_time()

        # computes TT
        for workshop in self.workshops:
            workshop.set_takt()

        # computes number of machines
        for workshop in self.workshops:
            workshop.set_machines()

        # computes sequences and setups
        for workshop in self.workshops:
            workshop.seq_calc()

        # computes operators
        for workshop in self.workshops:
            workshop.set_operators()

        # generates PMIM
        workshops = set()
        for part in self.visits:
            for seq in self.visits[part]:
                workshops.add(self.visits[part][seq]['w'])
        pmim = nestdict()
        for part in self.visits:
            for seq in self.visits[part]:
                for ws in workshops:
                    if self.visits[part][seq]['w'] == ws:
                        pmim[part][ws] = 1
                    else:
                        if pmim[part][ws] == 1:
                            pass
                        else:
                            pmim[part][ws] = 0
        # REMEMEMBER: HOW TO CONVERT DDICT TO DICT???
        pmim = ddict2dict(pmim)
        self.pmim = pmim

        # similarity matrix according to different algorithms
        sim_1 = {}
        for ws in workshops:
            parts_list = []
            for part in self.pmim:
                if self.pmim[part][ws] == 1:
                    parts_list.append(part)
            sim_1.update({ws: parts_list})

        # could have done that with pmim
        bar_urb = {}
        for ws in sim_1:
            sim_mtx_vals = {}
            for ws2 in sim_1:
                a = 0
                b = 0
                c = 0
                d = 0
                for part in self.visits:
                    if part in sim_1[ws] and part in sim_1[ws2]:
                        a = a + 1
                    elif part in sim_1[ws] and part not in sim_1[ws2]:
                        b = b + 1
                    elif part not in sim_1[ws] and part in sim_1[ws2]:
                        c = c + 1
                    elif part not in sim_1[ws] and part not in sim_1[ws2]:
                        d = d + 1
                sim = (a + math.sqrt(a * d)) / (a + b + c + math.sqrt(a * d))
                sim_mtx_vals.update({ws2: sim})
            bar_urb.update({ws: sim_mtx_vals})
        self.baroni_urbani = bar_urb

        ws_combs = []
        for ws in workshops:
            for ws2 in workshops:
                ws_combs.append((ws, ws2))

        # sintetic version of visits
        sint_visits = {}
        for part in self.visits:
            sint_phases = []
            for phase in self.visits[part]:
                sint_phases.append([self.visits[part][phase]['w'], self.visits[part][phase]['t']])
            sint_visits.update({part: sint_phases})

        gupt_seiff = {}
        for couple in ws_combs:
            num = 0
            den = 0
            for part in self.pmim:
                t = 0
                z = 0
                if self.pmim[part][couple[0]] == 1 and self.pmim[part][couple[1]] == 1:
                    x = 1
                    y = 0
                elif self.pmim[part][couple[0]] == 0 and self.pmim[part][couple[1]] == 0:
                    x = 0
                    y = 0
                else:
                    x = 0
                    y = 1
                if x == 1:
                    t0 = 0
                    t1 = 0
                    for el in sint_visits[part]:
                        if couple[0] == el[0]:
                            t0 = t0 +el[1]
                        if couple[1] == el[0]:
                            t1 = t1 + el[1]
                    t = min(t0, t1)/max(t0, t1)
                    for el, el2 in zip(sint_visits[part], sint_visits[part][1:]):
                        if (el[0] and el2[0]) in couple:
                            z = z + 1
                xxt = x * t
                num = num + (xxt + z) * self.demands[part]
                den = den + (xxt + z + y) * self.demands[part]
            gupt_seiff.update({couple: num/den})
        gupt_seiff_df = pd.DataFrame(index=workshops, columns=workshops)
        for el in gupt_seiff:
            gupt_seiff_df.at[el[0], el[1]] = gupt_seiff[el]

        self.gupt_seiff = gupt_seiff_df









