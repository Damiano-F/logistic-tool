from dfops import cross_sum
from dictops import maximum_keys
from operator import itemgetter

def layout(from_to):

    # sets diagonal flows to 0
    for el in from_to.columns:
        from_to.at[el, el] = 0
    # sums intercellular or interworkshop flows
    flows_sum = (from_to.sum()).sum()

    # TOTAL FLOW METHOD
    def total_flow_method(from_to):

        # sum of flows in the original matrix
        tot_flows = {}
        for idx in from_to.columns:
            tot_flow = cross_sum(from_to, idx, idx, False)
            tot_flows.update({idx: tot_flow})
        # max value of sum
        max = maximum_keys(tot_flows)

        # creates lists of sequences for each possible initial workshop/cell
        init = list(max[0])
        sequences = []
        for el in init:
            seq = []
            seq.append(el)
            sequences.append(seq)

        # creates actual sequences
        for el in sequences:
            while len(el) < len(from_to.columns):
                score_register = {}
                for idx in from_to.columns:
                    tot_sum = 0
                    if idx in el:
                        pass
                    else:
                        for i in range(len(el)):
                            tot_sum = tot_sum + from_to.at[el[i], idx] + from_to.at[idx, el[i]]
                        score_register.update({idx: tot_sum})
                next_entrance = 'undefined'
                next = maximum_keys(score_register)
                for ele in next[0]:
                    next_entrance = ele
                el.append(next_entrance)

        # computes integral of flows
        returned_sequences = []
        for el in sequences:
            flows = 0
            flows_integral = 0
            for i in range(len(el)):
                j = 0
                while i-j > 0:
                    flows = flows + from_to.iloc[i, j] + from_to.iloc[j, i]
                    j = j + 1
                flows_perc = flows/flows_sum
                flows_integral = flows_integral + flows_perc
            ret = (el, flows_integral)
            returned_sequences.append(ret)

        # checks max integral value between sequences
        integr = 0
        for el in returned_sequences:
            if el[1] > integr:
                integr = el[1]

        # removes elements with integral value less then max
        for el in returned_sequences:
            if el[1] < integr:
                returned_sequences.remove(el)

        return returned_sequences

    def single_flow_method(from_to):

        # turns from-to matrix into a list of tuples with coordinates and value
        lst = []
        for c in from_to.columns:
            for r in from_to.index:
                if r != c:
                    lst.append((r, c, from_to.at[r, c]))

        # sort list based on values
        lst_sort = sorted(lst, key=itemgetter(2), reverse=True)

        seq = [lst_sort[0][0], lst_sort[0][1]]

        # adds elements to the sequence
        while len(seq) < len(from_to.columns):
            for el in lst_sort:
                if el[0] in seq and el[1] not in seq:
                    seq.append(el[1])
                elif el[0] not in seq and el[1] in seq:
                    seq.append(el[0])

        # computes integral of flows
        flows = 0
        flows_integral = 0
        for i in range(len(seq)):
            j = 0
            while i-j > 0:
                flows = flows + from_to.iloc[i, j] + from_to.iloc[j, i]
                j = j + 1
                flows_perc = flows/flows_sum
                flows_integral = flows_integral + flows_perc
            returned_sequence = (seq, flows_integral)

        return returned_sequence

    total = total_flow_method(from_to)
    single = single_flow_method(from_to)

    # creates list of sequences with their flows integral values
    seq_compare = []
    seq_compare.append(single)
    for el in total:
        seq_compare.append(el)

    # selects sequences with higher integral
    max_seq = max(seq_compare, key=itemgetter(1))

    return max_seq[0]