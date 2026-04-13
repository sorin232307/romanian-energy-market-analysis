import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df_pret = pd.read_csv("Date_curate/preturi_energie_lunare.csv")
df_hidro = pd.read_csv("Date_curate/productie_hidro_lunara.csv")
df_euro = pd.read_csv("Date_curate/eur_ron_lunar.csv")
df_entsoe = pd.read_csv("date_complete.csv")

df = pd.merge(df_pret, df_hidro, on=["an", "luna"], how="inner")
df = pd.merge(df, df_euro[["an", "luna", "eur_ron_mediu"]], on=["an", "luna"], how="inner")

cols_to_use = [c for c in df_entsoe.columns if c not in df.columns or c in ["an", "luna"]]
df = pd.merge(df, df_entsoe[cols_to_use], on=["an", "luna"], how="inner")

df_annual = df.groupby('an').agg({
    'productie_hidro_totala_mwh': 'sum',
    'pret_energie_ron_mwh': 'mean',
    'eur_ron_mediu': 'mean'
}).reset_index()

sns.set_theme(style="dark", rc={
    "axes.facecolor": "#1c1c1c",
    "figure.facecolor": "#1c1c1c",
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "#bdbdbd",
    "ytick.color": "#bdbdbd",
    "grid.color": "#2d2d2d",
    "axes.edgecolor": "#2d2d2d"
})

flier_cfg = {"markerfacecolor": "cyan", "markeredgecolor": "white", "markersize": 6}

fig1, axes1 = plt.subplots(1, 2, figsize=(16, 6))
sns.histplot(df['pret_energie_ron_mwh'], kde=True, color="#9b59b6", ax=axes1[0], bins=30)
axes1[0].set_title("Distributia Pretului (RON/MWh)", fontsize=14, fontweight='bold')
sns.histplot(df['productie_hidro_totala_mwh'], kde=True, color="#3498db", ax=axes1[1], bins=30)
axes1[1].set_title("Distributia Productiei Hidro (MWh)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 6))
sns.boxplot(data=df, x='luna', y='pret_energie_ron_mwh', palette="flare", flierprops=flier_cfg)
plt.title("Variatia Lunara a Pretului Energiei (Sezonalitate)", fontsize=16, fontweight='bold')
plt.show()

plt.figure(figsize=(14, 6))
sns.boxplot(data=df, x='luna', y='productie_hidro_totala_mwh', palette="crest", flierprops=flier_cfg)
plt.title("Variatia Lunara a Productiei Hidro (Sezonalitate)", fontsize=16, fontweight='bold')
plt.show()

plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=df_annual,
    x="productie_hidro_totala_mwh",
    y="pret_energie_ron_mwh",
    size="eur_ron_mediu",
    color="#9b59b6",
    alpha=0.9,
    sizes=(100, 600),
    edgecolor="white",
    linewidth=1.5
)
for i in range(df_annual.shape[0]):
    plt.text(df_annual.productie_hidro_totala_mwh[i], df_annual.pret_energie_ron_mwh[i] + 15,
             str(int(df_annual.an[i])), color='white', fontsize=10, fontweight='bold', ha='center')
plt.title("Analiza Anuala: Productie Totala vs. Pret Mediu", fontsize=16, fontweight='bold')
plt.show()

fig2, axes2 = plt.subplots(2, 1, figsize=(14, 12))
sns.boxplot(data=df, x='an', y='pret_energie_ron_mwh', palette="flare", ax=axes2[0], flierprops=flier_cfg)
axes2[0].set_title("Distributia Pretului pe Ani", fontsize=14, fontweight='bold')
sns.boxplot(data=df, x='an', y='productie_hidro_totala_mwh', palette="crest", ax=axes2[1], flierprops=flier_cfg)
axes2[1].set_title("Distributia Productiei pe Ani", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 12))
cols_to_corr = [c for c in df.select_dtypes(include=[np.number]).columns if c not in ['an', 'luna']]
corr = df[cols_to_corr].corr()
sns.heatmap(corr, annot=True, cmap="magma", fmt=".2f", linewidths=0.5,
            cbar_kws={"shrink": .8}, annot_kws={"size": 8})
plt.title("Matricea de Corelatie Completa", fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.show()