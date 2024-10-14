import pandas as pd

data = pd.read_csv('6(10) complete.csv')
df = data.drop(data.columns[-1], axis=1)
df.to_csv('6(10) complete.csv', index=False)   