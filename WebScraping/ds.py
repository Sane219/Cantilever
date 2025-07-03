import pandas as pd
df = pd.read_excel('data/ebay_data.xlsx')
print(df.head())
print(df['price'].head())
print(df['rating'].head())