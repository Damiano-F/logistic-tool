from dfops import cross_sum
from dictops import maximum_keys

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

        for el in sequences:
            flows_percent = 0
            for el2, el3 in zip(el, el[1:]):
                flows_percent = flows_percent + (from_to.at[el2, el3] + from_to.at[el3, el2])/flows_sum
                print(el2, el3, flows_percent)

        return 0

    total_flow_method(from_to)