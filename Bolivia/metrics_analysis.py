"""
mae_train_analysis.py
=====================
Calcula MAE de entrenamiento del modelo MLP-BP+PCA (primer bloque, sin lag features)
replicando exactamente el pipeline de Modelamiento.py lineas 630-920.
"""

import warnings; warnings.filterwarnings("ignore")
import sys; sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error

BASE = "C:/Users/juans/Downloads/Avances_tesis/Bolivia/"

# 1. Cargar datos
social_norm = pd.read_excel(BASE + "SocialMedia_FinalDataset.xlsx")
social_norm["date"] = pd.to_datetime(social_norm["date"])

# 2. Encuestas y resultado
polls = pd.DataFrame({
    "fecha": pd.to_datetime([
        "2025-05-26","2025-06-14","2025-06-20",
        "2025-07-07","2025-07-10","2025-07-27","2025-07-28",
        "2025-08-03","2025-08-04","2025-08-06",
        "2025-09-25","2025-10-06","2025-10-07","2025-10-09"
    ]),
    "Quiroga": [65,78,59,64,73,69,81,71,86,71,47.0,44.4,42.9,44.9],
    "Paz":     [15,20,23,11,14,20,27,23,32,29,39.3,36.2,38.7,36.5]
})
election_date   = pd.Timestamp("2025-10-18")
election_result = {"Quiroga": 45.47, "Paz": 54.53}
real_paz        = election_result["Paz"] / 100

# 3. Interpolacion diaria
def daily_intent_from_polls(polls_df, elec_date, elec_result):
    rows = []
    for _, r in polls_df.iterrows():
        p = r["Paz"]/100 if r["Paz"]>1 else r["Paz"]
        q = r["Quiroga"]/100 if r["Quiroga"]>1 else r["Quiroga"]
        s = p + q
        rows.append({"fecha": r["fecha"], "Paz": p/s, "Quiroga": q/s})
    rows.append({"fecha": elec_date,
                 "Paz": elec_result["Paz"]/100,
                 "Quiroga": elec_result["Quiroga"]/100})
    df_p = pd.DataFrame(rows).sort_values("fecha").drop_duplicates("fecha")
    idx  = pd.date_range(df_p["fecha"].min(), df_p["fecha"].max(), freq="D")
    return (df_p.set_index("fecha").reindex(idx).interpolate("linear")
            .reset_index().rename(columns={"index":"fecha"}))

intento = daily_intent_from_polls(polls, election_date, election_result)
intento = intento.rename(columns={"fecha": "date"})

# 4. Dataset con target
df = social_norm.copy()
df["date"] = pd.to_datetime(df["date"])
df["IntencionVotoReal"] = np.nan
for cand in ["Paz", "Quiroga"]:
    serie = intento.set_index("date")[cand]
    m = df["account"].str.lower() == cand.lower()
    df.loc[m, "IntencionVotoReal"] = df.loc[m, "date"].map(serie)
df = df.sort_values(["account", "date"])

# 5. Separar train/pred (PRIMER BLOQUE — sin lag features)
first_poll = polls["fecha"].min()
last_poll  = polls["fecha"].max()
mask_paz   = df["account"].str.lower() == "paz"
mask_train_window = (df["date"] >= first_poll) & (df["date"] <= last_poll)
mask_pred_window  = df["date"] <= election_date

X_all = df.select_dtypes(include=[np.number]).drop(columns=["IntencionVotoReal"], errors="ignore")
y_all = df["IntencionVotoReal"]

train_idx_paz = mask_paz & mask_train_window & y_all.notna()
pred_idx_paz  = mask_paz & mask_pred_window

X_train_paz = X_all.loc[train_idx_paz]
y_train_paz = y_all.loc[train_idx_paz].values
X_pred_paz  = X_all.loc[pred_idx_paz]
dates_paz   = df.loc[pred_idx_paz, "date"].values

print(f"Training points (Paz): {len(y_train_paz)}")
print(f"Prediction points (Paz): {len(dates_paz)}")

# 6. Escalar (fit solo en entrenamiento)
scaler = StandardScaler().fit(X_train_paz)
Xs_tr  = scaler.transform(X_train_paz)
Xs_pp  = scaler.transform(X_pred_paz)

# 7. PCA
n_comp = min(6, Xs_tr.shape[1])
pca    = PCA(n_components=n_comp).fit(Xs_tr)
Xtr_p  = pca.transform(Xs_tr)
Xpp_p  = pca.transform(Xs_pp)

# 8. Entrenar MLP-BP + PCA
print("Entrenando MLP-BP + PCA...")
mlp = MLPRegressor(
    hidden_layer_sizes=(48,24), activation="relu",
    solver="adam", learning_rate_init=3e-4,
    alpha=0.02, max_iter=4000, random_state=42
)
mlp.fit(Xtr_p, y_train_paz)

# 9. Predicciones sobre toda la ventana
raw_pred = np.clip(mlp.predict(Xpp_p), 0, 1)
pred_suav = raw_pred.copy()
for i in range(2, len(pred_suav)):
    dp = pred_suav[i-1] - pred_suav[i-2]
    dn = raw_pred[i]    - pred_suav[i-1]
    beta = 0.8 if np.sign(dp) != np.sign(dn) else 0.6
    pred_suav[i] = beta*pred_suav[i-1] + (1-beta)*raw_pred[i]

pred_series = pd.Series(pred_suav, index=pd.to_datetime(dates_paz))

# 10. Predicciones sobre datos de entrenamiento
pred_train_raw  = np.clip(mlp.predict(Xtr_p), 0, 1)
y_pred_train    = pred_train_raw  # sin suavizado (para comparacion limpia)
mae_train_insample = mean_absolute_error(y_train_paz, y_pred_train)

# 11. MAE_test (dia de eleccion)
pred_eleccion = pred_series.get(election_date, np.nan)
mae_test      = abs(pred_eleccion - real_paz) if not np.isnan(pred_eleccion) else np.nan

# 12. MAE sobre fechas de encuesta reales
polls_paz    = polls[["fecha","Paz"]].copy()
polls_paz["Paz_frac"] = polls_paz["Paz"]/100
polls_paz["fecha"]    = pd.to_datetime(polls_paz["fecha"])
pred_on_polls = pred_series.reindex(polls_paz["fecha"])
y_true_polls  = polls_paz.set_index("fecha")["Paz_frac"]
mask_pv       = pred_on_polls.notna() & y_true_polls.notna()
mae_encuestas = mean_absolute_error(y_true_polls[mask_pv], pred_on_polls[mask_pv])

# 13. Reporte
print("\n" + "="*65)
print("METRICAS COMPARATIVAS — MLP-BP + PCA — Candidato Paz")
print("="*65)
print(f"\n  Prediccion dia eleccion: {pred_eleccion:.4f} ({pred_eleccion*100:.2f}%)")
print(f"  Resultado real:          {real_paz:.4f} ({real_paz*100:.2f}%)")
print()
print(f"  MAE_test     (OUT-OF-SAMPLE — dia eleccion):      {mae_test:.4f}  ({mae_test*100:.2f} pp)")
print(f"  MAE_train    (IN-SAMPLE — datos de entrenamiento):{mae_train_insample:.4f}  ({mae_train_insample*100:.2f} pp)")
print(f"  MAE_encuestas(IN-SAMPLE — fechas de encuesta):    {mae_encuestas:.4f}  ({mae_encuestas*100:.2f} pp)")
print()
ratio_te = mae_test / mae_train_insample if mae_train_insample > 0 else float("inf")
ratio_ep = mae_test / mae_encuestas if mae_encuestas > 0 else float("inf")
print(f"  Ratio MAE_test / MAE_train:     {ratio_te:.2f}x")
print(f"  Ratio MAE_test / MAE_encuestas: {ratio_ep:.2f}x")
print()
if ratio_ep < 2:
    msg = "El modelo generaliza razonablemente bien. El error fuera de muestra no es desproporcionado."
elif ratio_ep < 4:
    msg = "Brecha moderada tren/prueba, razonable para n_train pequeno."
else:
    msg = "Gran brecha — el punto de prueba podria ser atipico."
print(f"  Interpretacion: {msg}")
print("="*65)
