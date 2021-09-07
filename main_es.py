from loader import Loader
from plant import Plant
from cost_calc import LogistiCalc

loader_ = Loader(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\cycles_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\demand_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\bom_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\workshops_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\vehicles_sample.xlsx')

plant = Plant(loader_)
vehicles = plant.vehicles

cost = LogistiCalc(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\times_sample.xlsx',
                   r'C:\Users\damia\OneDrive\Desktop\logistic management tool\fromto_sample.xlsx',
                   vehicles)