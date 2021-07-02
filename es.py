from loader import Loader
from plant import Plant

cycles = r'C:\Users\damia\OneDrive\Desktop\logistic management tool\Es1\cycles_sample.xlsx'
demand = r'C:\Users\damia\OneDrive\Desktop\logistic management tool\Es1\demand_sample.xlsx'
bom = r'C:\Users\damia\OneDrive\Desktop\logistic management tool\Es1\bom_sample.xlsx'
workshops = r'C:\Users\damia\OneDrive\Desktop\logistic management tool\Es1\workshops_sample.xlsx'

loader_ = Loader(cycles, demand, bom, workshops)

plant = Plant(loader_)