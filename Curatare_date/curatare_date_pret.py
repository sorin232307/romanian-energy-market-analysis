import pandas as pd
import glob
import os

fisiere = glob.glob("date_brute/entso_preturi/*.csv")
print(f"Fisiere gasite: {len(fisiere)}")

lista_df = []
for fisier in fisiere:
    df_temp = pd.read_csv(fisier, sep=",", quotechar='"', encoding="utf-8-sig")
    lista_df.append(df_temp)

df_preturi = pd.concat(lista_df, ignore_index=True)

df_preturi = df_preturi[["MTU (CET/CEST)", "Day-ahead Price (RON/MWh)", "Day-ahead Price (EUR/MWh)"]].copy()

df_preturi = df_preturi.rename(columns={
    "MTU (CET/CEST)": "mtu",
    "Day-ahead Price (RON/MWh)": "pret_ron",
    "Day-ahead Price (EUR/MWh)": "pret_eur"
})

df_preturi["pret_ron"] = pd.to_numeric(df_preturi["pret_ron"], errors="coerce")
df_preturi["pret_eur"] = pd.to_numeric(df_preturi["pret_eur"], errors="coerce")

df_preturi["data"] = df_preturi["mtu"].str.split(" - ").str[0]
df_preturi["data"] = df_preturi["data"].str.replace(r"\s*\(CET\)|\s*\(CEST\)", "", regex=True).str.strip()
df_preturi["data"] = pd.to_datetime(df_preturi["data"], format="%d/%m/%Y %H:%M:%S")
df_preturi["an"] = df_preturi["data"].dt.year
df_preturi["luna"] = df_preturi["data"].dt.month

df_preturi_lunar = df_preturi.groupby(["an", "luna"])[["pret_ron", "pret_eur"]].mean().reset_index()

df_curs = pd.read_csv("date_curate/eur_ron_lunar.csv")

df_rezultat = pd.merge(df_preturi_lunar, df_curs, on=["an", "luna"], how="left")

df_rezultat["pret_ron"] = df_rezultat["pret_ron"].fillna(
    df_rezultat["pret_eur"] * df_rezultat["eur_ron_mediu"]
)

print("Valori lipsa pret_ron:", df_rezultat["pret_ron"].isna().sum())

df_rezultat = df_rezultat[["an", "luna", "pret_ron"]]
df_rezultat.columns = ["an", "luna", "pret_energie_ron_mwh"]

print(df_rezultat.head(12))
print(f"\nDimensiune: {df_rezultat.shape}")
print(df_rezultat.groupby("an")["luna"].count())

os.makedirs("date_curate", exist_ok=True)
df_rezultat.to_csv("date_curate/preturi_energie_lunare.csv", index=False)
print("\nFisier salvat: date_curate/preturi_energie_lunare.csv")