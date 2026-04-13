import pandas as pd

df = pd.read_csv("../Date_brute/Hidroelectrica/hidroelectrica_financiar.csv")

print(df.head(3))
print("\nDimensiune")
print(df.shape)
print("Coloane", df.columns.tolist())
print("\nTipuri variabile")
print(df.dtypes)

print("\nNumar ani: ", len(df))
print("\nValoare maxima: ", df["venituri_mil_ron"].max())

print(df.loc[df["venituri_mil_ron"].idxmax()])
print(df.loc[df["venituri_mil_ron"].idxmin()])

df.to_csv("Date_curate/financiar_hidro.csv", index = False )