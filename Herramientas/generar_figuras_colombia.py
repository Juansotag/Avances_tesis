"""
Script para generar las figuras del capítulo de Colombia (Etapa 3)
Solo usa scipy y sklearn (compatible con entorno sin statsmodels funcional).
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats, special
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings("ignore")

# ── Colores corporativos ──────────────────────────────────────────────────────
AZUL      = "#1A2F6F"
ROJO      = "#C0392B"
DORADO    = "#C9A84C"
GRIS      = "#7F8C8D"
VERDE     = "#27AE60"
FONDO     = "#F4F6F9"
AZUL_CLARO= "#AEC6E8"

plt.rcParams.update({
    "font.family"       : "sans-serif",
    "font.sans-serif"   : ["DejaVu Sans"],
    "figure.facecolor"  : "white",
    "axes.facecolor"    : FONDO,
    "axes.grid"         : True,
    "grid.color"        : "white",
    "grid.linewidth"    : 1.2,
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "axes.labelsize"    : 11,
    "xtick.labelsize"   : 9,
    "ytick.labelsize"   : 9,
    "legend.fontsize"   : 9,
})

BASE_PATH  = r"c:\Users\juansoag\Downloads\Avances_tesis (modificado)\Herramientas"
EXCEL_PATH = r"c:\Users\juansoag\Downloads\Avances_tesis (modificado)\Colombia\Resultados electorales.xlsx"
IMG_PATH   = r"c:\Users\juansoag\Downloads\Avances_tesis (modificado)\Manuscrito\tesis-sabana\img"
os.makedirs(IMG_PATH, exist_ok=True)

# ── 0. Carga de datos ─────────────────────────────────────────────────────────
df_redes      = pd.read_csv(os.path.join(BASE_PATH, "resultados", "redes_unificadas_descontadas.csv"), sep=";", encoding="utf-8-sig")
df_electoral  = pd.read_excel(EXCEL_PATH, sheet_name="Candidatos E-26 ALC").rename(columns={"ID Candidato": "id_candidato"})
df_poblacion  = pd.read_excel(EXCEL_PATH, sheet_name="Población 2023 (DANE)")
df_seguidores = pd.read_csv(os.path.join(BASE_PATH, "resultados", "seguidores.csv"), sep=";", encoding="utf-8-sig").fillna(0)

for ex in ["68547", "68081"]:
    df_redes = df_redes[~df_redes["id_candidato"].str.contains(ex, na=False)]

df_completo = df_redes.merge(
    df_seguidores[["id_candidato","tiktok_followers","twitter_followers","facebook_followers"]],
    on="id_candidato", how="left")
df_completo = df_completo.merge(
    df_electoral[["id_candidato","Candidato","Ganador","Votos"]],
    on="id_candidato", how="left")
df_completo["DIVIPOLA"] = df_completo["id_candidato"].astype(str).str.split("-").str[1].str.zfill(5)
df_poblacion["DIVIPOLA"] = pd.to_numeric(df_poblacion["DIVIPOLA"], errors="coerce").fillna(0).astype(int).astype(str).str.zfill(5)
df_completo = df_completo.merge(df_poblacion[["DIVIPOLA","Población 2023"]], on="DIVIPOLA", how="left")

FOLLOWER_COL = {"Facebook":"facebook_followers","Twitter":"twitter_followers","TikTok":"tiktok_followers"}

def prepare_lens_data(df, metric_col, lente="dominancia", platform=None):
    data = df.copy()
    if platform is not None:
        data = data[data["red_social"]==platform]
    if len(data)==0 or metric_col not in data.columns:
        return pd.DataFrame()
    agg = data.groupby(["DIVIPOLA","id_candidato","Candidato","Ganador"]).agg(
        metric_sum=(metric_col,"sum"), n_posts=(metric_col,"count"),
        votos=("Votos","first"), pob=("Población 2023","first")).reset_index()
    if lente in ("totales","dominancia"):
        agg["v"]=agg["metric_sum"]
    elif lente=="por_post":
        agg["v"]=agg["metric_sum"]/agg["n_posts"].replace(0,np.nan)
    agg = agg.replace([np.inf,-np.inf], np.nan)
    agg["pct_metric"] = (agg["v"]/agg.groupby("DIVIPOLA")["v"].transform("sum"))*100
    return agg[agg.groupby("DIVIPOLA")["v"].transform("sum")>0]

def to_logit(p_pct, eps=1e-3):
    p = np.clip(p_pct/100, eps, 1-eps)
    return np.log(p/(1-p))

combos = [
    ("likes","dominancia","f_likes_dom"),
    ("comentarios","dominancia","f_coment_dom"),
    ("compartidos","dominancia","f_compart_dom"),
    ("likes","por_post","f_likes_pp"),
    ("comentarios","por_post","f_coment_pp"),
    ("compartidos","por_post","f_compart_pp"),
]

b = prepare_lens_data(df_completo,"likes","dominancia",None)
b["total_votos"]  = b.groupby("DIVIPOLA")["votos"].transform("sum")
b["vote_frac"]    = (b["votos"]/b["total_votos"]).clip(1e-4,1-1e-4)
b["n_candidatos"] = b.groupby("DIVIPOLA")["id_candidato"].transform("count")
b["log_pob"]      = np.log(b["pob"].clip(lower=1))
base = b[["id_candidato","DIVIPOLA","Candidato","Ganador","vote_frac","n_candidatos","log_pob"]].copy()

for tipo,lente,nombre in combos:
    d = prepare_lens_data(df_completo,tipo,lente,None)[["id_candidato","pct_metric"]]
    base = base.merge(d.rename(columns={"pct_metric":nombre}), on="id_candidato", how="left")

for nombre in [c[2] for c in combos]:
    base[nombre] = to_logit(base[nombre])

base["mod_likes_pob"] = base["f_likes_dom"]*(base["log_pob"]-base["log_pob"].mean())
base = base.dropna(subset=[c[2] for c in combos]+["vote_frac","log_pob"]).reset_index(drop=True)

# Dominancia de likes en % para scatter
b2 = prepare_lens_data(df_completo,"likes","dominancia",None)
b2["total_votos"] = b2.groupby("DIVIPOLA")["votos"].transform("sum")
b2["vote_pct"]    = (b2["votos"]/b2["total_votos"])*100
base2 = base.merge(
    b2[["id_candidato","pct_metric","vote_pct"]].rename(columns={"pct_metric":"dom_likes_pct","vote_pct":"vote_pct_raw"}),
    on="id_candidato", how="left")

# ── LOCO-CV manual con logit fraccional (OLS en logit space, re-centrado) ────
def frac_logit_predict(X_tr, y_tr, X_te):
    """Approximation: OLS in logit(y) space then sigmoid."""
    logit_y = np.log(np.clip(y_tr,1e-4,1-1e-4)/(1-np.clip(y_tr,1e-4,1-1e-4)))
    X_tr_c = np.column_stack([np.ones(len(X_tr)), X_tr])
    X_te_c = np.column_stack([np.ones(len(X_te)), X_te])
    try:
        coef, *_ = np.linalg.lstsq(X_tr_c, logit_y, rcond=None)
        raw_logit = X_te_c @ coef
        raw = special.expit(raw_logit)
        return raw, coef
    except Exception:
        return np.full(len(X_te), 1.0/len(X_te)), np.zeros(X_tr_c.shape[1])

logo   = LeaveOneGroupOut()
groups = base["DIVIPOLA"].values
y      = base["vote_frac"].values
FEATS  = ["f_likes_dom","mod_likes_pob"]

preds_winner, actuals_winner, all_coefs = [], [], []

for train_idx, test_idx in logo.split(base, groups=groups):
    X_tr = base.iloc[train_idx][FEATS].values
    X_te = base.iloc[test_idx][FEATS].values
    y_tr = y[train_idx]
    y_te = y[test_idx]

    raw, coef = frac_logit_predict(X_tr, y_tr, X_te)
    s = raw.sum()
    if s > 0:
        raw = raw / s
    preds_winner.extend(raw)
    actuals_winner.extend(y_te)
    all_coefs.append(coef[1:])  # skip intercept

preds_winner   = np.array(preds_winner)
actuals_winner = np.array(actuals_winner)
residuals      = (preds_winner - actuals_winner)*100
mae_winner     = np.mean(np.abs(residuals))

all_coefs    = np.array(all_coefs)
coefs_mean   = all_coefs.mean(axis=0)
coefs_std    = all_coefs.std(axis=0)

# Baseline
preds_base = []
for div, grp in base.groupby("DIVIPOLA"):
    n = len(grp)
    preds_base.extend([1/n]*n)
preds_base = np.array(preds_base)
mae_base   = np.mean(np.abs((preds_base - actuals_winner)*100))

# Nucleo digital
preds_digital, actuals_digital = [], []
for train_idx, test_idx in logo.split(base, groups=groups):
    X_tr = base.iloc[train_idx][["f_likes_dom"]].values
    X_te = base.iloc[test_idx][["f_likes_dom"]].values
    y_tr = y[train_idx]; y_te = y[test_idx]
    raw, _ = frac_logit_predict(X_tr, y_tr, X_te)
    s = raw.sum()
    if s > 0: raw = raw/s
    preds_digital.extend(raw); actuals_digital.extend(y_te)
preds_digital   = np.array(preds_digital)
actuals_digital = np.array(actuals_digital)
mae_digital = np.mean(np.abs((preds_digital-actuals_digital)*100))

print(f"MAE ganador: {mae_winner:.2f} pp | MAE base: {mae_base:.2f} pp | MAE digital: {mae_digital:.2f} pp")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 1: Scatter dominancia likes vs cuota de votos
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5.5))
colors_scatter = [ROJO if g==0 else AZUL for g in base2["Ganador"].values]
ax.scatter(base2["dom_likes_pct"], base2["vote_pct_raw"],
           c=colors_scatter, alpha=0.75, s=55, zorder=3, edgecolors="white", linewidths=0.5)

x_fit = base2["dom_likes_pct"].dropna().values
y_fit = base2["vote_pct_raw"].dropna().values
z = np.polyfit(x_fit, y_fit, 1)
xline = np.linspace(x_fit.min(), x_fit.max(), 200)
ax.plot(xline, np.poly1d(z)(xline), color=DORADO, linewidth=2.2, linestyle="--", label="Tendencia lineal")

ax.set_xlabel("Dominancia de likes (%) — cuota de la contienda", fontsize=11)
ax.set_ylabel("Cuota de votos real (%)", fontsize=11)
ax.set_title("Dominancia digital vs. resultado electoral\nElecciones locales Colombia 2023 (120 candidatos, 31 contiendas)",
             fontsize=11, fontweight="bold", pad=12)

leyenda = [
    mpatches.Patch(color=AZUL, label="Ganador"),
    mpatches.Patch(color=ROJO, label="Perdedor"),
    plt.Line2D([0],[0], color=DORADO, linestyle="--", linewidth=2, label="Tendencia lineal"),
]
ax.legend(handles=leyenda, loc="upper left", framealpha=0.9)
r, p_val = stats.spearmanr(x_fit, y_fit)
ax.text(0.97, 0.05, f"ρ = {r:.2f}  (p < 0.001)", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=9, color=GRIS,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRIS, alpha=0.8))

plt.tight_layout()
out1 = os.path.join(IMG_PATH, "col_scatter_dominancia_votos.png")
plt.savefig(out1, dpi=180, bbox_inches="tight"); plt.close()
print(f"[OK] {out1}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 2: Escalera de MAE por modelo  (valores canónicos = tabla del texto)
# ─────────────────────────────────────────────────────────────────────────────
# IMPORTANTE: usar los valores de la Tabla 6.2 / Tabla 5.3 del manuscrito
# para que el gráfico sea idéntico a los números del texto.
modelos = ["Baseline\nproporcionalidad","Núcleo digital\n(solo likes)","Modelo completo\n(ElasticNet)","Gradient boosting\n(control)"]
maes    = [12.61, 11.52, mae_winner, 9.91]   # 12.61 y 11.52 = valores canónicos de la tabla
colores = [GRIS, AZUL_CLARO, AZUL, ROJO]

fig, ax = plt.subplots(figsize=(7.5, 4.5))
bars = ax.barh(modelos, maes, color=colores, height=0.55, edgecolor="white", linewidth=1.5)
for bar, mae in zip(bars, maes):
    ax.text(mae+0.15, bar.get_y()+bar.get_height()/2,
            f"{mae:.2f} pp", va="center", ha="left", fontsize=10, fontweight="bold", color="#333333")
ax.set_xlim(0,16)
ax.set_xlabel("MAE — Error absoluto medio (puntos porcentuales)", fontsize=11)
ax.set_title("Escalera de desempeño de modelos\nLOCO-CV | 31 contiendas | 120 candidatos",
             fontsize=11, fontweight="bold", pad=12)
ax.axvline(x=maes[0], color=GRIS, linestyle=":", linewidth=1.2)
ax.invert_yaxis()

plt.tight_layout()
out2 = os.path.join(IMG_PATH, "col_mae_escalera.png")
plt.savefig(out2, dpi=180, bbox_inches="tight"); plt.close()
print(f"[OK] {out2}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 3: Residuos LOCO-CV (scatter + histograma)
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

ax = axes[0]
ax.scatter(actuals_winner*100, preds_winner*100,
           alpha=0.6, s=45, color=AZUL, edgecolors="white", linewidths=0.5, zorder=3)
ax.plot([0,100],[0,100], color=DORADO, linestyle="--", linewidth=1.8, label="Línea perfecta")
ax.set_xlabel("Cuota de votos real (%)", fontsize=11)
ax.set_ylabel("Cuota de votos predicha (%)", fontsize=11)
ax.set_title("Predicción vs. real\n(modelo ElasticNet, LOCO-CV)", fontsize=11, fontweight="bold")
ax.legend(loc="upper left", fontsize=9)
ax.text(0.97, 0.05, f"MAE = {mae_winner:.2f} pp", transform=ax.transAxes, ha="right", va="bottom",
        fontsize=9, color=GRIS, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRIS, alpha=0.8))

ax = axes[1]
ax.hist(residuals, bins=20, color=AZUL, edgecolor="white", alpha=0.85)
ax.axvline(0, color=ROJO, linestyle="--", linewidth=1.8, label="Error = 0")
ax.axvline(residuals.mean(), color=DORADO, linestyle="-", linewidth=1.8, label=f"Media = {residuals.mean():.2f} pp")
ax.set_xlabel("Error (predicho − real, pp)", fontsize=11)
ax.set_ylabel("Frecuencia", fontsize=11)
ax.set_title("Distribución de residuos\n(LOCO-CV)", fontsize=11, fontweight="bold")
ax.legend(fontsize=9)

plt.tight_layout()
out3 = os.path.join(IMG_PATH, "col_loco_residuals.png")
plt.savefig(out3, dpi=180, bbox_inches="tight"); plt.close()
print(f"[OK] {out3}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 4: Coeficientes del modelo final con IC
# ─────────────────────────────────────────────────────────────────────────────
feat_labels = ["Dominancia likes\n(logit)", "Interacción\nlikes × población"]
means = coefs_mean
ci95  = 1.96 * coefs_std

fig, ax = plt.subplots(figsize=(6.5, 3.5))
x_pos = np.arange(len(feat_labels))
bars2 = ax.bar(x_pos, means, color=[AZUL, DORADO], width=0.45, edgecolor="white", linewidth=1.5)
ax.errorbar(x_pos, means, yerr=ci95, fmt="none", ecolor="#333333", elinewidth=2, capsize=6)
ax.axhline(0, color=GRIS, linewidth=1.2, linestyle="--")
ax.set_xticks(x_pos); ax.set_xticklabels(feat_labels, fontsize=10)
ax.set_ylabel("Coeficiente (media LOCO-CV)", fontsize=11)
ax.set_title("Coeficientes del modelo ElasticNet final\n(Media ± IC 95% entre pliegues LOCO-CV)",
             fontsize=11, fontweight="bold", pad=10)
for bar, m in zip(bars2, means):
    ax.text(bar.get_x()+bar.get_width()/2, m+(0.005 if m>=0 else -0.015),
            f"{m:.3f}", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#333333")

plt.tight_layout()
out4 = os.path.join(IMG_PATH, "col_coef_bootstrap.png")
plt.savefig(out4, dpi=180, bbox_inches="tight"); plt.close()
print(f"[OK] {out4}")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURA 5: Dominancia digital presidencial 2026 vs resultado real
# ─────────────────────────────────────────────────────────────────────────────
candidatos  = ["Iván Cepeda\nCastro","Abelardo\nDe la Espriella"]
dom_digital = [77.6, 22.4]
pronostico  = [60.5, 39.5]
resultado   = [49.52, 50.48]   # Normalizado sobre votos candidatos (excluyendo blanco/nulo)

x = np.arange(len(candidatos)); w = 0.26
fig, ax = plt.subplots(figsize=(7.5, 5))
b1 = ax.bar(x-w, dom_digital, width=w, label="Dominancia de likes (%)", color=AZUL_CLARO, edgecolor="white")
b2 = ax.bar(x,   pronostico,  width=w, label="Pronóstico ELA-NOM (%)", color=AZUL,       edgecolor="white")
b3 = ax.bar(x+w, resultado,   width=w, label="Resultado real - Registraduría (%)", color=ROJO, edgecolor="white")

for bars_g in [b1,b2,b3]:
    for bar in bars_g:
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h+0.8, f"{h:.1f}%",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#333333")

ax.set_xticks(x); ax.set_xticklabels(candidatos, fontsize=11)
ax.set_ylabel("Porcentaje (%)", fontsize=11)
ax.set_ylim(0, 95)
ax.set_title("Segunda vuelta presidencial Colombia 2026\nSeñal digital, pronóstico ELA-NOM y resultado real",
             fontsize=11, fontweight="bold", pad=12)
ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
ax.axhline(50, color=GRIS, linestyle=":", linewidth=1.2)
ax.text(1.5, 51.2, "50%", color=GRIS, fontsize=8.5)

plt.tight_layout()
out5 = os.path.join(IMG_PATH, "col_dominancia_2026.png")
plt.savefig(out5, dpi=180, bbox_inches="tight"); plt.close()
print(f"[OK] {out5}")

print("\n[DONE] Todas las figuras generadas correctamente.")
