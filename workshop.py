import math
import numpy as np

from iteration_utilities import unique_everseen

class Workshop:

    def __init__(self, name, shifts, shift_dur, pauses, pause_dur, placing, type_, uptime):

        self.name = name
        self.shifts = shifts
        self.shift_dur = shift_dur
        self.pauses = pauses
        self.pause_dur = pause_dur
        self.placing = placing
        self.type_ = type_
        self.uptime = uptime

        self.parts = []
        self.automation = 'undefined'
        self.disp_time = 'undefined'
        self.takt_time = 'undefined'
        self.prod_time = 'undefined'
        self.utilization = 'undefined'
        self.machines = 'undefined'
        self.setup_1seq = 'undefined'
        self.n_seq = 'undefined'
        self.operators = 'undefined'
        self.op_util = 'undefined'


    def set_part(self, part):

        self.parts.append(part)

    def set_automation(self):

        automation = []
        for part in self.parts:
            for phase in part.phases:
                if phase.placings > 0:
                    automation.append(1)
                elif phase.placings == 0 and phase.machining != phase.operator:
                    automation.append(2)
                elif phase.placings == 0 and phase.machining == phase.operator:
                    automation.append(3)
                else:
                    raise Exception('Undefined type for workshop, part, phase: ', self.name, part.name, phase.seq)

        automation = list(unique_everseen(automation))

        if 3 in automation and 2 in automation:
            automation.remove(3)

        if len(automation) != 1:
            raise Exception('more that 1 kind of automation: ', self.automation, self.name)

        self.automation = automation[0]

    # computes workshop disposable time
    def set_disp_time(self):

        if self.automation == 3:
            # better to do total time * uptime - pauses or (total time - pauses) * uptime?
            self.disp_time = self.shifts * self.shift_dur * 60 * self.uptime - self.pauses * self.pause_dur * self.shifts
        # is it ok to put together machine and auto?
        elif self.automation == 2 or self.automation == 1:
            self.disp_time = self.shifts * self.shift_dur * 60 * self.uptime
        else:
            raise Exception('Undefined disposable time for: ', self.name, self.automation)

    def set_takt(self):

        tot_demand = 0
        for part in self.parts:
            tot_demand = tot_demand + part.demand

        self.takt_time = self.disp_time/tot_demand

    def set_machines(self):

        if self.automation == 3 and self.type_ == 'in-out':
            prod_time = 0
            for part in self.parts:
                for phase in part.phases:
                    prod_time = prod_time + part.demand * phase.operator
        elif self.automation == 3 and self.type_ == 'queue':
            prod_time = self.disp_time
        else:
            prod_time = 0
            for part in self.parts:
                for phase in part.phases:
                    prod_time = prod_time + part.demand * (phase.machining + phase.operator)

        self.prod_time = prod_time
        self.utilization = self.prod_time/self.disp_time
        self.machines = math.ceil(prod_time/self.disp_time)

    def seq_calc(self):

        setup_sum = 0
        for part in self.parts:
            for phase in part.phases:
                setup_sum = setup_sum + phase.setup

        self.setup_1seq = setup_sum

        demands = {p.name: p.demand for p in self.parts}

        if setup_sum == 0:
            tts = {p: self.disp_time / demands[p] for p in demands}
            n_seq = math.ceil(self.disp_time / max(tts.values()))
            ratios = {p: max(tts.values()) / tts[p] for p in tts}
        elif setup_sum > 0:
            n_seq1 = (self.disp_time * self.machines - self.prod_time) / setup_sum
            if n_seq1 > 1:
                n_seq = math.ceil(n_seq1)
                ratios = {p: demands[p]/n_seq for p in demands}
            else:
                self.machines = self.machines + 1
                n_seq = math.ceil((self.disp_time * self.machines - self.prod_time) / setup_sum)
                ratios = {p: demands[p]/n_seq for p in demands}

        self.n_seq = n_seq

        ceil = {p: math.ceil(ratios[p]) for p in ratios}
        floor = {p: math.floor(ratios[p]) for p in ratios}

        splits = {}
        for p in ratios:
            if ceil[p] != floor[p]:
                split = np.linalg.solve([[floor[p], ceil[p]], [1, 1]], [demands[p], n_seq])
                splits.update({p: {'min': [floor[p], round(split[0])], 'max': [ceil[p], round(split[1])]}})
            else:
                split = n_seq
                splits.update({p: split})

        return {self.name: splits}

    def set_operators(self):

        if self.automation == 1:
            num = 0
            for part in self.parts:
                for phase in part.phases:
                    num = num + self.placing * phase.placings * part.demand
            den = 60 * self.shift_dur
            operators = num/den
            self.operators = math.ceil(operators)
            self.op_util = operators/self.operators
        else:
            num = 0
            for part in self.parts:
                for phase in part.phases:
                    num = num + part.demand * phase.operator
            num = num + self.setup_1seq * self.n_seq
            den = self.shifts * (self.shift_dur * 60 - self.pauses * self.pause_dur)
            operators = num/den
            self.operators = math.ceil(operators)
            if self.operators < self.shifts:
                self.operators = self.shifts
            self.op_util = operators/self.operators


