import pandas as pd
from dictops import nestdict
from sim_matrix import gupta_seiffodini
from clustering import clusters

class Plant:

    def __init__(self, loader):

        self.loader = loader
        self.workshops = self.loader.get_workshops()
        self.visits = self.loader.get_visits()
        self.demands = self.loader.get_demands()

        self.pmim = 'undefined'
        self.sim_matrix = 'undefined'
        self.clusters = 'undefined'

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
        self.pmim = pd.DataFrame.from_dict(pmim)

        self.sim_matrix = gupta_seiffodini(workshops, self.pmim, self.visits, self.demands)

        self.clusters = clusters(self.sim_matrix, 'average')
        print(self.clusters)