import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import Lasso, ElasticNet
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df0 = pd.read_csv("Date_curate/preturi_energie_lunare.csv")
df1 = pd.read_csv("Date_curate/productie_hidro_lunara.csv")
df2 = pd.read_csv("Date_curate/eur_ron_lunar.csv")
variabile_independente = ["productie_hidro_totala_mwh", "eur_ron_mediu", "hidro_reservoir_mwh", "criza_energetica"]
df3 = pd.merge(df0 , df1, on = ["an", "luna"], how = "inner")
df = pd.merge(df3, df2, on = ["an", "luna"], how = "inner")
df["criza_energetica"] = (df["an"].isin([2022, 2023])).astype(int)

X = df[variabile_independente]
Y = df["pret_energie_ron_mwh"]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)

rf = RandomForestRegressor(n_estimators = 100, random_state = 42)
rf.fit(X_train, Y_train)
y_pred_rf = rf.predict(X_test)

lasso = Lasso(alpha=0.1)
lasso.fit(X_train, Y_train)
y_pred_lasso = lasso.predict(X_test)

en = ElasticNet(alpha=0.1)
en.fit(X_train, Y_train)
y_pred_en = en.predict(X_test)

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

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

modele = ["Random Forest", "Lasso", "ElasticNet"]
mae_valori = [
    mean_absolute_error(Y_test, y_pred_rf),
    mean_absolute_error(Y_test, y_pred_lasso),
    mean_absolute_error(Y_test, y_pred_en)
]
sns.barplot(x=modele, y=mae_valori, palette="magma", ax=axes[0])
axes[0].set_title("Comparație Eroare (MAE)", fontsize=14, fontweight='bold')
axes[0].set_ylabel("RON")

importanta = pd.DataFrame({
    "variabila": variabile_independente,
    "importanta": rf.feature_importances_
}).sort_values("importanta", ascending=True)
sns.barplot(data=importanta, x="importanta", y="variabila", palette="flare", ax=axes[1])
axes[1].set_title("Importanța Factorilor (RF)", fontsize=14, fontweight='bold')

sns.scatterplot(x=Y_test, y=y_pred_rf, color="#9b59b6", alpha=0.7, s=100, ax=axes[2])
sns.lineplot(x=[Y_test.min(), Y_test.max()], y=[Y_test.min(), Y_test.max()], color="white", linestyle="--", ax=axes[2])
axes[2].set_title("Real vs. Prezis (Random Forest)", fontsize=14, fontweight='bold')
axes[2].set_xlabel("Valori Reale")
axes[2].set_ylabel("Predicție")

plt.tight_layout()
plt.show()

print(f"R2 RF: {r2_score(Y_test, y_pred_rf):.4f}")
print(f"R2 Lasso: {r2_score(Y_test, y_pred_lasso):.4f}")
print(f"R2 EN: {r2_score(Y_test, y_pred_en):.4f}")