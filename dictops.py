from collections import defaultdict
import collections
import json

def nestdict():
    return collections.defaultdict(nestdict)

# NOT WORKING RIGHT NOW!!
def ddict2dict(d):
    return json.loads(json.dumps(d))

# NOT WORKING RIGHT NOW!!
def dict_format(d, el):
    d2 = d.copy()
    return d2.pop(el)

def maximum_keys(dic):
    maximum = max(dic.values())
    keys = [k for k, v in dic.items() if v == maximum]
    return keys,maximum

def max_nested(dic):

    maxdict = {}
    for el in dic:
        maximum = max(dic[el].values())
        for el2 in dic[el]:
            if dic[el][el2] == maximum and el != el2:
                maxdict.update({(el, el2): maximum})

    abs_max = maximum_keys(maxdict)

    return abs_max

def remove_as_df(dic, el):

    def_dic = defaultdict(float, dic)

    for item in def_dic:
        if item == el:
            pass
        else:
            for item2 in def_dic[item]:
                if item2 == el:
                    del def_dic[item][item2]

    return dic

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value
