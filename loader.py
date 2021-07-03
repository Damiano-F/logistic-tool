import pandas as pd
import numpy as np
import math
from iteration_utilities import duplicates, unique_everseen, flatten
from workshop import Workshop


class Phase:

    def __init__(self, seq, workshop, machining, operator, placings, setup):

        self.seq = seq
        self.workshop = workshop
        self.machining = machining
        self.operator = operator
        self.placings = placings
        self.setup = setup


class Part:

    def __init__(self, name, phases, workshop):

        self.name = name
        self.phases = phases
        self.workshop = workshop
        self.demand = 'undefined'

        # check if all seq are unique and in sequence
        if not all(x.seq < y.seq for x, y in zip(self.phases, self.phases[1:])):
            raise Exception('Unsorted phases in part: ', self.name)

    def set_demand(self, demand):
        self.demand = demand

class Vehicle:

    def __init__(self, name, capacity):

        self.name = name
        self.capacity = capacity

class Loader:

    def __init__(self, cycles_file, demand_file, bom_file, workshops_file, vehicles_file):

        self.cycles_file = cycles_file
        self.demand_file = demand_file
        self.bom_file = bom_file
        self.workshops_file = workshops_file
        self.vehicles_file = vehicles_file

        self.demands = 'undefined'
        self.workshops = []
        self.parts_visits = 'undefined'
        self.vehicles = 'undefined'

        cycles = pd.read_excel(self.cycles_file, sheet_name=None)
        # checks if all part names are unique
        cycles_names = []
        for sheet in cycles:
            cycles_names.append(cycles[sheet].columns[0])
        if list(duplicates(cycles_names)):
            raise Exception('Multiple parts names in cycles file: ', list(duplicates(cycles_names)))
        # list of parts sheets
        sheets = []
        for sheet in cycles:
            sheets.append(cycles[sheet])
        # fillna
        sheets = [sheets[i].fillna(0) for i in range(len(sheets))]
        # drops useless 2nd row
        sheets = [sheets[i].drop([0]) for i in range(len(sheets))]
        # drops useless columns
        sheets = [sheets[i].drop(['Unnamed: 1', 'T mac (min/pz)', 'Unnamed: 4', 'Unnamed: 5'], axis=1) for i in range(len(sheets))]
        # list of parts
        parts = []
        for sheet in sheets:
            part_name = sheet.columns[0]
            workshops_set = set()
            phases_list = []
            for i in range(len(sheet.index)):
                seq = sheet.iloc[i][0]
                workshop = sheet.iloc[i][1]
                workshops_set.add(workshop)
                machining = sheet.iloc[i][2]
                operator = sheet.iloc[i][3]
                placings = sheet.iloc[i][4]
                setup = sheet.iloc[i][5]
                # checks placings coherence
                if (placings > 0 and setup > 0) or (placings > 0 and operator > 0):
                    raise Exception('Placing coherence error in part, phase: ', part_name, seq)
                phase = Phase(seq, workshop, machining, operator, placings, setup)
                phases_list.append(phase)
            for workshop in workshops_set:
                same_workshop_phases = []
                for phase in phases_list:
                    if workshop == phase.workshop:
                        same_workshop_phases.append(phase)
                part = Part(part_name, same_workshop_phases, workshop)
                parts.append(part)

        # defines visiting sequences
        parts_visits = {}
        for sheet in sheets:
            name = sheet.columns[0]
            visit_seq = {}
            for i in range(len(sheet.index)):
                seq = sheet.iloc[i][0]
                workshop = sheet.iloc[i][1]
                machining = sheet.iloc[i][2]
                visit_seq.update({seq: {'w': workshop, 't': machining}})
            parts_visits.update({name: visit_seq})
        self.parts_visits = parts_visits

        demand_data = pd.read_excel(self.demand_file)
        demand_data = demand_data.fillna(0)
        # checks for multiple products
        if list(duplicates(demand_data)):
            raise Exception('Multiple parts in demand file: ', list(duplicates(demand_data)))

        bom_data = pd.read_excel(self.bom_file)
        bom_data = bom_data.fillna(0)
        # changes index name from numbers to parts
        new_indexes = []
        for item in bom_data['Unnamed: 0']:
            new_indexes.append(item)
        bom_data.index = new_indexes
        # deletes parts names column
        bom_data = bom_data.drop(['Unnamed: 0'], axis=1)
        # checks for multiple parts in rows and columns
        if list(duplicates(bom_data.columns)):
            raise Exception('Multiple parts in BoM columns: ', list(duplicates(bom_data.columns)))
        if list(duplicates(bom_data.index)):
            raise Exception('Multiple parts in BoM rows: ', list(duplicates(bom_data.index)))
        # checks coherence of parts data
        bom_parts = list(unique_everseen(list(bom_data.columns) + list(bom_data.index)))
        for el in bom_parts:
            if el not in cycles_names:
                raise Exception('Part from BoM not present in cycles data: ', el)
        for el in cycles_names:
            if el not in bom_parts:
                raise Exception('Part from cycles data not present in BoM: ', el)
        # removes non numerical elements
        for row in bom_data.index:
            for col in bom_data.columns:
                if row == col:
                    bom_data.at[row, col] = 0

        # CHECKS FOR RECURSIVE DEPENDENCIES
        paths = []
        for part in bom_data.columns:
            path = [part]
            paths.append(path)

        idxs = []
        for idx in bom_data.index:
            idxs.append(idx)

        def dependencies_check(paths, idxs, results):

            parts = []
            for path in paths:
                if path[-1] in list(bom_data.columns):
                    parts.append(path[-1])
                else:
                    results.append(path)

            if not parts:
                return results
            else:
                filt_paths = []
                for part in parts:
                    for path in paths:
                        if path[-1] == part:
                            filt_paths.append(path)

                requirings = {}
                for path in filt_paths:
                    requiring = []
                    for idx in idxs:
                        if bom_data.at[idx, path[-1]] > 0:
                            requiring.append(idx)
                    requirings.update({path[-1]: requiring})

                new_paths = []
                for path in paths:
                    for el in requirings:
                        if path[-1] == el:
                            for val in requirings[el]:
                                new_path = []
                                new_path.append(path)
                                new_path = list(flatten(new_path))
                                new_path.append(val)
                                new_paths.append(new_path)

                for path in new_paths:
                    if list(duplicates(path)):
                        raise Exception('duplicates in path: ', path)

                dependencies_check(new_paths, idxs, results)

        results = []
        dependencies_check(paths, idxs, results)

        # DEMAND COMPUTATION AND ASSIGNMENT
        paths_by_parts = []
        for part in demand_data.columns:
            for el in results:
                if part in el:
                    i = el.index(part)
                    comb = el[:i+1]
                    paths_by_parts.append(comb)
        paths_by_parts = list(unique_everseen(paths_by_parts))

        def demand_calculator(parts_names, paths, demand_data, bom_data):

            constants = []
            for name in parts_names:
                const = 0
                for path in paths:
                    if len(path) == 1 and path[0] == name:
                        const = int(demand_data.loc[:, name])
                constants.append(const)

            lst = {}
            for name in parts_names:
                group = {}
                for name2 in parts_names:
                    group.update({name2: []})
                lst.update({name: group})

            for el in lst:
                for el2 in lst[el]:
                    for path in paths:
                        if path[-1] == el and path[0] == el2:
                            lst[el][el2].append(path)

            for el in lst:
                for el2 in lst[el]:
                    if el == el2:
                        lst[el].update({el2: 1})
                    elif not lst[el][el2] :
                        lst[el].update({el2: 0})
                    else:
                        sum_const = 0
                        for path in lst[el][el2]:
                            const = -1
                            for col, row in zip(path, path[1:]):
                                const = const * bom_data.at[row, col]
                            sum_const = sum_const + const
                        lst[el].update({el2: sum_const})

            factors = []
            for el in lst:
                factors_split = []
                for el2 in lst[el]:
                    factors_split.append(lst[el][el2])
                factors.append((factors_split))

            demands = dict(zip(parts_names, np.linalg.solve(factors, constants)))
            for el in demands:
                demands.update({el: math.ceil(demands[el])})
            return demands

        self.demands = demand_calculator(cycles_names, paths_by_parts, demand_data, bom_data)

        # demand assignment
        for part in parts:
            for el in self.demands:
                if part.name == el:
                    part.set_demand(self.demands[el])

        workshops_data = pd.read_excel(self.workshops_file, sheet_name=None)
        # checks if there are turns and turn durations
        for workshop in workshops_data:
            if int(workshops_data[workshop]['Shifts']) == 0:
                raise Exception('Missing shifts in workshop: ', workshop)
            if float(workshops_data[workshop]['Shift duration (h)']) == 0:
                raise Exception('Missing Shift duration in workshop: ', workshop)
        # checks for multiple names
        if list(duplicates(workshops_data)):
            raise Exception('Duplicate names in workshops data: ', list(duplicates(workshops_data)))
        # checks if all the workshops in the parts are present in the workshop file
        for part in parts:
            for phase in part.phases:
                if phase.workshop not in workshops_data:
                    raise Exception('workshop in cycles not found in workshops file: ', phase.workshop)
        # creates workshop obj
        for workshop in workshops_data:
            name = workshop
            shifts = int(workshops_data[workshop]['Shifts'])
            shift_dur = float(workshops_data[workshop]['Shift duration (h)'])
            pauses = int(workshops_data[workshop]['Pauses/shift'])
            pause_dur = float(workshops_data[workshop]['Pause duration (min)'])
            placing = float(workshops_data[workshop]['Placing duration (min)'])
            type_ = str(workshops_data[workshop].at[0, 'Type'])
            uptime = float(workshops_data[workshop]['uptime'])
            workshop = Workshop(name, shifts, shift_dur, pauses, pause_dur, placing, type_, uptime)
            self.workshops.append(workshop)

        # setting parts for workshops
        for part in parts:
            for workshop in self.workshops:
                if workshop.name == part.workshop:
                    workshop.set_part(part)

        #loading vehicles informations
        vehicles_data = pd.read_excel(self.vehicles_file)
        vehicles = []
        for i in vehicles_data.index:
            name = vehicles_data.at[i, 'Vehicle']
            capacity = vehicles_data.iloc[:, 1:8]
            for col in capacity.columns:
                if 'P1' in col: capacity.rename(columns={col: 'Part1'}, inplace=True)
                elif 'P2' in col: capacity.rename(columns={col: 'Part2'}, inplace=True)
                elif 'P3' in col: capacity.rename(columns={col: 'Part3'}, inplace=True)
                elif 'P4' in col: capacity.rename(columns={col: 'Part4'}, inplace=True)
                elif 'P5' in col: capacity.rename(columns={col: 'Part5'}, inplace=True)
                elif 'P6' in col: capacity.rename(columns={col: 'Part6'}, inplace=True)
                elif 'P7' in col: capacity.rename(columns={col: 'Part7'}, inplace=True)
            vehicle = Vehicle(name, capacity)
            vehicles.append(vehicle)

        self.vehicles = vehicles


    def get_workshops(self):
        return self.workshops

    def get_visits(self):
        return self.parts_visits

    def get_demands(self):
        return self.demands

    def get_vehicles(self):
        return self.vehicles
