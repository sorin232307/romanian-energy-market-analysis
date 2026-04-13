import pandas as pd
import glob


cale_fisiere = "/Users/sorin__/PycharmProjects/ProiectPachete/Date_brute/Generation/20*.csv"
fisiere_generare = glob.glob(cale_fisiere)

lista_df = []
for fisier in fisiere_generare:
    print(f"Citesc {fisier}...")
    df_temp = pd.read_csv(fisier)
    lista_df.append(df_temp)

df = pd.concat(lista_df, ignore_index=True)

df['Generation (MW)'] = pd.to_numeric(df['Generation (MW)'].replace(['n/e', 'n/a'], pd.NA), errors='coerce')

df.dropna(subset=['Generation (MW)'], inplace=True)

df['Data_Start'] = df['MTU (UTC)'].str.split(' - ').str[0]
df['Data_End'] = df['MTU (UTC)'].str.split(' - ').str[1]

df['Data_Start'] = pd.to_datetime(df['Data_Start'], format='%d/%m/%Y %H:%M:%S')
df['Data_End'] = pd.to_datetime(df['Data_End'], format='%d/%m/%Y %H:%M:%S')

df['an'] = df['Data_Start'].dt.year
df['luna'] = df['Data_Start'].dt.month

df['Durata_ore'] = (df['Data_End'] - df['Data_Start']).dt.total_seconds() / 3600
df['Generation_MWh'] = df['Generation (MW)'] * df['Durata_ore']

df_lunar = df.groupby(['an', 'luna', 'Production Type'])['Generation_MWh'].sum().unstack().reset_index()

nume_noi = {col: col.lower().replace(' ', '_').replace('-', '_').replace('/', '_')
            for col in df_lunar.columns if col not in ['an', 'luna']}
df_lunar.rename(columns=nume_noi, inplace=True)

if 'hydro_run_of_river_and_pondage' in df_lunar.columns and 'hydro_water_reservoir' in df_lunar.columns:
    df_lunar['productie_hidro_totala_mwh'] = df_lunar['hydro_run_of_river_and_pondage'] + df_lunar['hydro_water_reservoir']

df_lunar = df_lunar.fillna(0)

for col in df_lunar.columns:
    df_lunar[col] = df_lunar[col].astype(int)

nume_fisier_final = "productie_lunara_entsoe_toate.csv"
df_lunar.to_csv(nume_fisier_final, index=False)

print(list(df_lunar.columns))