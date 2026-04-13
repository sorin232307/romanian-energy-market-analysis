import pandas as pd

df_bnr = pd.read_csv("../Date_brute/BNR/curs_valutar.csv")
print("----DATE BRUTE----")
print(df_bnr.head(5))
print(df_bnr.dtypes)

df_bnr.columns = ["data", "eur_ron", "variatie_lei", "variatie_proc"]

luni_ro_en = {
    "Sept": "Sep",  "Mart": "Mar", "Ian": "Jan", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr", "Mai": "May", "Iun": "Jun", "Iul": "Jul",
    "Aug": "Aug","Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dec": "Dec"
}

for ro, en in luni_ro_en.items():
    df_bnr["data"] = df_bnr["data"].str.replace(ro, en, regex = False)

df_bnr["data"] = df_bnr["data"].str.replace(".", "", regex = False)
df_bnr["data"] = pd.to_datetime(df_bnr["data"], format="%d %b %Y", errors = "coerce")

print("\nDupa conversii:")
print(df_bnr.dtypes)
print(df_bnr.head(5))

df_bnr = df_bnr[
    (df_bnr["data"].dt.year >= 2015) &
    (df_bnr["data"].dt.year <= 2025)
]

print("\nDupa filtrare ani:", df_bnr.shape)

df_bnr["an"] = df_bnr["data"].dt.year
df_bnr["luna"] = df_bnr["data"].dt.month

df_bnr_lunar = df_bnr.groupby(["an", "luna"])["eur_ron"].mean().reset_index()
df_bnr_lunar.columns = ["an", "luna", "eur_ron_mediu"]

print("\nDate curate")
print(df_bnr.head(12))
print("\nDimensiune finala", df_bnr_lunar.shape)

df_bnr_lunar.to_csv("date_curate/eur_ron_lunar.csv", index = False)

print(df_bnr_lunar.groupby("an")["luna"].count())

