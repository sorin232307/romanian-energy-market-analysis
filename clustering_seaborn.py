import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df0 = pd.read_csv("Date_curate/productie_hidro_lunara.csv")
df1 = pd.read_csv("Date_curate/preturi_energie_lunare.csv")
df2 = pd.read_csv("Date_curate/eur_ron_lunar.csv")

df = pd.merge(df0, df1, on=["an", "luna"], how="inner")
df = pd.merge(df, df2, on=["an", "luna"], how="inner")

X = df[["productie_hidro_totala_mwh", "pret_energie_ron_mwh", "eur_ron_mediu"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

sns.set_theme(style="dark", rc={
    "axes.facecolor": "#212121",
    "figure.facecolor": "#212121",
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "#bdbdbd",
    "ytick.color": "#bdbdbd",
    "grid.color": "#424242",
    "axes.edgecolor": "#424242"
})

plt.figure(figsize=(12, 8))

sns.scatterplot(
    data=df,
    x="productie_hidro_totala_mwh",
    y="pret_energie_ron_mwh",
    hue="cluster",
    size="eur_ron_mediu",
    palette="flare",
    alpha=0.8,
    sizes=(50, 250),
    edgecolor="#424242",
    linewidth=0.5
)

plt.title("Analiza Clusterelor: Regimuri de Producție vs. Preț", fontsize=16, fontweight='bold', color='white')
plt.xlabel("Producție Hidro (MWh)", color='white')
plt.ylabel("Preț Energie (RON/MWh)", color='white')

leg = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', facecolor='#212121', edgecolor='#424242')
plt.setp(leg.get_texts(), color='white')
plt.setp(leg.get_title(), color='white')

plt.tight_layout()
plt.show()

print(df.groupby("cluster")[["productie_hidro_totala_mwh", "pret_energie_ron_mwh", "eur_ron_mediu"]].mean().round(2))
print(df[df["cluster"] == 1]["an"].value_counts().sort_index())