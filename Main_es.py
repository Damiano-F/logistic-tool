from loader import Loader
from plant import Plant

loader_ = Loader(r'C:\Users\damia\OneDrive\Desktop\logistic management tool\cycles_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\demand_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\bom_sample.xlsx',
                 r'C:\Users\damia\OneDrive\Desktop\logistic management tool\workshops_sample.xlsx')

plant = Plant(loader_)