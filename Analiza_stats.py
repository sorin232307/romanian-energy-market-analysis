import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("Date_curate/date_analiza_finala.csv")

#print("Perioada Acoperita:", df["an"].min()," - ",  df["an"].max())
#print("\nNumar de observatii:", df.shape)
pd.set_option("display.float_format", lambda x: f"{x:.2f}")
#print("\nStatistic descriptive: ", df.describe().T.to_string())
#eur_ron cea mai stabila, iar pret_energie cea mai volatila

variabile_independente = ["productie_hidro_totala_mwh", "pret_energie_ron_mwh", "eur_ron_mediu"]

#descrieri = {"productie_hidro_totala_mwh": "Productie hidroenergetica totala (MWh)","pret_energie_ron_mwh": "Pretul mediu al energiei electrice (RON/MWh)","eur_ron_mediu": "Cursul mediu de schimb EUR/RON"}

#print(df["profit_net_mil_ron"].count())

X = df[variabile_independente]
X = sm.add_constant(X)
Y = df["venituri_mil_ron"]

model = sm.OLS(Y, X)
rezultate = model.fit()
print(rezultate.summary())

print("\n--- Interpretarea coeficientilor ---")
for variabila, coef in zip(variabile_independente, rezultate.params[1:]):
    print(f"{variabila}: {coef:.4f}")

    