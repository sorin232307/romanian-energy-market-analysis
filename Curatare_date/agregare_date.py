import pandas as pd

df_prod = pd.read_csv("../Date_curate/productie_hidro_lunara.csv")
df_pret = pd.read_csv("../Date_curate/preturi_energie_lunare.csv")
df_eur_ron = pd.read_csv("../Date_curate/eur_ron_lunar.csv")
df_hidro = pd.read_csv("../Date_curate/financiar_hidro.csv")

df_prod_anual = df_prod.groupby("an")["productie_hidro_totala_mwh"].sum().reset_index()
df_pret_anual = df_pret.groupby("an")["pret_energie_ron_mwh"].mean().reset_index()
df_eur_ron_anual = df_eur_ron.groupby("an")["eur_ron_mediu"].mean().reset_index()


df_merged = pd.merge(df_hidro, df_prod_anual, on = "an", how = "inner")
df_merged2 = pd.merge(df_merged, df_pret_anual, on = "an", how = "inner")
df_merged_final = pd.merge(df_merged2, df_eur_ron_anual, on = "an", how = "inner")

print(df_merged_final.head())
print(df_merged_final.columns)
print(df_merged_final.shape)
df_merged_final.to_csv("Date_curate/date_analiza_finala.csv", index = False)