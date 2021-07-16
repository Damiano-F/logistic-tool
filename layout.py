from dfops import cross_sum
from dictops import maximum_keys

def layouts(from_to):

    flows_list = []
    for el in from_to:
        tot_flows = {}
        for idx in el.columns:
            tot_flow = cross_sum(el, idx, idx, False)
            tot_flows.update({idx: tot_flow})
        flows_list.append(tot_flows)

    max_cells = []
    for el in flows_list:
        max = maximum_keys(el)
        max_cells.append(max)
    print(max_cells)