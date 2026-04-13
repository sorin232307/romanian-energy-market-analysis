import pandas as pd
import glob

cale_load = "/Users/sorin__/PycharmProjects/ProiectPachete/Date_brute/Load/*.csv"
fisiere_load = glob.glob(cale_load)

lista_df = []
for f in fisiere_load:
    lista_df.append(pd.read_csv(f))

df_load = pd.concat(lista_df, ignore_index=True)

col_load = [col for col in df_load.columns if 'Actual Total Load' in col][0]

df_load[col_load] = pd.to_numeric(
    df_load[col_load].astype(str).str.replace(',', '').replace(['n/e', 'n/a', 'N/A', '-'], pd.NA),
    errors='coerce'
)

df_load.dropna(subset=[col_load], inplace=True)
df_load['Data_Start'] = df_load['MTU (UTC)'].str.split(' - ').str[0]
df_load['Data_End'] = df_load['MTU (UTC)'].str.split(' - ').str[1]

df_load['Data_Start'] = pd.to_datetime(df_load['Data_Start'], format='%d/%m/%Y %H:%M', errors='coerce')
df_load['Data_End'] = pd.to_datetime(df_load['Data_End'], format='%d/%m/%Y %H:%M', errors='coerce')

df_load.dropna(subset=['Data_Start', 'Data_End'], inplace=True)

df_load['an'] = df_load['Data_Start'].dt.year
df_load['luna'] = df_load['Data_Start'].dt.month

df_load['Durata_ore'] = (df_load['Data_End'] - df_load['Data_Start']).dt.total_seconds() / 3600
df_load['cerere_nationala_mwh'] = df_load[col_load] * df_load['Durata_ore']

df_load_lunar = df_load.groupby(['an', 'luna'])['cerere_nationala_mwh'].sum().reset_index()
df_load_lunar['cerere_nationala_mwh'] = df_load_lunar['cerere_nationala_mwh'].astype(int)

df_prod = pd.read_csv("productie_lunara_entsoe_toate.csv")

df_final = pd.merge(df_prod, df_load_lunar, on=['an', 'luna'], how='inner')

nume_baza_finala = "date_complete.csv"
df_final.to_csv(nume_baza_finala, index=False)

print(df_final[['an', 'luna', 'cerere_nationala_mwh', 'productie_hidro_totala_mwh', 'wind_onshore']].head())