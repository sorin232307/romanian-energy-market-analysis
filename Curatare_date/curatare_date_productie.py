import pandas as pd
import glob
import os

fisiere = glob.glob("Date_brute/entso_productie/*.csv")

lista_df = []
for fisier in fisiere:
    df_temp = pd.read_csv(fisier, sep=",", quotechar='"', encoding="utf-8-sig")
    lista_df.append(df_temp)

df_productie = pd.concat(lista_df, ignore_index=True)

tipuri_hidro = ["Hydro Run-of-river and pondage", "Hydro Water Reservoir"]
df_hidro = df_productie[df_productie["Production Type"].isin(tipuri_hidro)].copy()

df_hidro["Generation (MW)"] = pd.to_numeric(df_hidro["Generation (MW)"], errors="coerce")

df_hidro["data"] = df_hidro["MTU (CET/CEST)"].str.split(" - ").str[0]
df_hidro["data"] = df_hidro["data"].str.replace(r"\s*\(CET\)|\s*\(CEST\)", "", regex=True).str.strip()
df_hidro["data"] = pd.to_datetime(df_hidro["data"], format="%d/%m/%Y %H:%M:%S")

df_hidro["an"] = df_hidro["data"].dt.year
df_hidro["luna"] = df_hidro["data"].dt.month
df_hidro["durata_ore"] = df_hidro["an"].apply(lambda x: 1 if x <= 2021 else 0.25)
df_hidro["productie_mwh"] = df_hidro["Generation (MW)"] * df_hidro["durata_ore"]

df_hidro_lunar = df_hidro.groupby(
    ["an", "luna", "Production Type"]
)["productie_mwh"].sum().reset_index()

df_hidro_pivot = df_hidro_lunar.pivot_table(
    index=["an", "luna"],
    columns="Production Type",
    values="productie_mwh",
    aggfunc="sum"
).reset_index()

df_hidro_pivot.columns.name = None
df_hidro_pivot = df_hidro_pivot.rename(columns={
    "Hydro Run-of-river and pondage": "hidro_run_of_river_mwh",
    "Hydro Water Reservoir": "hidro_reservoir_mwh"
})

df_hidro_pivot["productie_hidro_totala_mwh"] = (
    df_hidro_pivot["hidro_run_of_river_mwh"].fillna(0) +
    df_hidro_pivot["hidro_reservoir_mwh"].fillna(0)
)

print(df_hidro_pivot.head(12))
print(df_hidro_pivot.shape)
print(df_hidro_pivot.groupby("an")["luna"].count())

os.makedirs("../Date_curate", exist_ok=True)
df_hidro_pivot.to_csv("Date_curate/productie_hidro_lunara.csv", index=False)
print("Fisier salvat: Date_curate/productie_hidro_lunara.csv")