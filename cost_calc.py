import pandas as pd

class LogistiCalc:

    def __init__(self, times_matrix, from_to, vehicles):

        self.times_matrix = 'undefined'
        self.from_to = 'undefined'
        self.vehicles = vehicles

        clean_times = pd.read_excel(times_matrix)
        clean_times = clean_times.drop(['Unnamed: 0'], axis=1)
        self.times_matrix = clean_times

        clean_ft = pd.read_excel(from_to)
        clean_ft = clean_ft.drop(['Unnamed: 0'], axis=1)
        self.from_to = clean_ft

        tot_times = self.times_matrix.mul(self.from_to)

