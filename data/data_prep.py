import pandas as pd

df = pd.read_csv("./data/raw data.csv")


commodities = [
    comodity + "-" + unit
    for comodity, unit in zip(df.commodity.to_list(), df.unit.to_list())
]

prices = df.price_cents.to_list()

nutrients_labels = df.columns[3:].to_list()

nutrients = []
for index, row in df.iterrows():
    nutrients.append(row.values[3:].tolist())

target_nutrients = [
    ["Calories (kcal)", 3],
    ["Protein (g)", 70],
    ["Calcium (g)", 0.8],
    ["Iron (mg)", 12],
    ["Vitamin A (KIU)", 5],
    ["Vitamin B1 (mg)", 1.8],
    ["Vitamin B2 (mg)", 2.7],
    ["Niacin (mg)", 18],
    ["Vitamin C (mg)", 75],
]
target_nutrients = [nutrient[1] for nutrient in target_nutrients]
