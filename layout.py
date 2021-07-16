from dfops import cross_sum
import pandas as pd

def layouts(from_to):

    flows_list = []
    for el in from_to:
        tot_flows = {}
        print(el)
        for idx in el.columns:
            tot_flow = cross_sum(el, idx, idx, False)
            tot_flows.update({idx: tot_flow})
        print(tot_flows)
        flows_list.append(tot_flows)

    print(flows_list)