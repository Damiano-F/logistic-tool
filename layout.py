from dfops import cross_sum

def layouts(from_to):

    tot_flows = {}
    for el in from_to:
        print(el)
        for idx in el.columns:
            print(type(idx))
            tot_flow = cross_sum(el, idx, idx)
            tot_flows.update({idx: tot_flow})
            print(tot_flow)

    print(tot_flows)