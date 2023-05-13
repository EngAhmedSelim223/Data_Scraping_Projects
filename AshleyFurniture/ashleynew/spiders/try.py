import pandas as pd

df = pd.read_excel("data.xlsx")
links = df['links']
for x in links:
    print(x)