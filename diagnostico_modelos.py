"""
diagnostico_modelos.py
Compara las tres implementaciones del LOCO-CV para encontrar la más precisa.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.linear_model import ElasticNetCV
from scipy import special
import statsmodels.api as sm

RAIZ         = Path(r'C:\Users\juans\Downloads\Avances_tesis')
HERRAMIENTAS = RAIZ / 'Herramientas'
REDES_TRAIN  = HERRAMIENTAS / 'resultados' / 'redes_unificadas.csv'
SEGUIDORES   = HERRAMIENTAS / 'resultados' / 'seguidores.csv'
EXCEL_PATH   = RAIZ / 'Colombia' / 'Resultados electorales.xlsx'

# ── Carga y preparación (igual al modelo) ─────────────────────────────────────
df_redes      = pd.read_csv(REDES_TRAIN, sep=';', encoding='utf-8-sig')
df_electoral  = pd.read_excel(EXCEL_PATH, sheet_name='Candidatos E-26 ALC').rename(columns={'ID Candidato': 'id_candidato'})
df_poblacion  = pd.read_excel(EXCEL_PATH, sheet_name='Población 2023 (DANE)')
df_seguidores = pd.read_csv(SEGUIDORES, sep=';', encoding='utf-8-sig').fillna(0)

for ex in ['68547', '68081']:
    df_redes = df_redes[~df_redes['id_candidato'].str.contains(ex, na=False)]

df = df_redes.merge(df_seguidores[['id_candidato','tiktok_followers','twitter_followers','facebook_followers']], on='id_candidato', how='left')
df = df.merge(df_electoral[['id_candidato','Candidato','Ganador','Votos']], on='id_candidato', how='left')
df['DIVIPOLA'] = df['id_candidato'].astype(str).str.split('-').str[1].str.zfill(5)
df_poblacion['DIVIPOLA'] = pd.to_numeric(df_poblacion['DIVIPOLA'], errors='coerce').fillna(0).astype(int).astype(str).str.zfill(5)
df = df.merge(df_poblacion[['DIVIPOLA','Población 2023']], on='DIVIPOLA', how='left')

def prepare_lens_data(data, metric_col, lente='dominancia'):
    data = data.copy()
    agg = data.groupby(['DIVIPOLA','id_candidato','Candidato','Ganador']).agg(
        metric_sum=(metric_col,'sum'), n_posts=(metric_col,'count'),
        votos=('Votos','first'), pob=('Población 2023','first')).reset_index()
    if lente in ('totales','dominancia'): agg['v'] = agg['metric_sum']
    elif lente == 'por_post': agg['v'] = agg['metric_sum'] / agg['n_posts'].replace(0, np.nan)
    agg = agg.replace([np.inf,-np.inf], np.nan)
    agg['pct_metric'] = (agg['v'] / agg.groupby('DIVIPOLA')['v'].transform('sum')) * 100
    return agg[agg.groupby('DIVIPOLA')['v'].transform('sum') > 0]

def to_logit(p_pct, eps=1e-3):
    p = np.clip(p_pct / 100, eps, 1 - eps)
    return np.log(p / (1 - p))

b = prepare_lens_data(df, 'likes', 'dominancia')
b['total_votos'] = b.groupby('DIVIPOLA')['votos'].transform('sum')
b['vote_frac']   = (b['votos'] / b['total_votos']).clip(1e-4, 1 - 1e-4)
b['n_candidatos']= b.groupby('DIVIPOLA')['id_candidato'].transform('count')
b['log_pob']     = np.log(b['pob'].clip(lower=1))
base = b[['id_candidato','DIVIPOLA','Candidato','Ganador','vote_frac','n_candidatos','log_pob']].copy()

combos = [('likes','dominancia','f_likes_dom'),('comentarios','dominancia','f_coment_dom'),
          ('compartidos','dominancia','f_compart_dom'),('likes','por_post','f_likes_pp'),
          ('comentarios','por_post','f_coment_pp'),('compartidos','por_post','f_compart_pp')]
for tipo, lente, nombre in combos:
    d = prepare_lens_data(df, tipo, lente)[['id_candidato','pct_metric']]
    base = base.merge(d.rename(columns={'pct_metric': nombre}), on='id_candidato', how='left')
for nombre in [c[2] for c in combos]:
    base[nombre] = to_logit(base[nombre])
base['mod_likes_pob'] = base['f_likes_dom'] * (base['log_pob'] - base['log_pob'].mean())
base = base.dropna(subset=[c[2] for c in combos] + ['vote_frac','log_pob']).reset_index(drop=True)

FEATS = ['f_likes_dom', 'mod_likes_pob']
X = base[FEATS].values.astype(float)
y = base['vote_frac'].values
g = base['DIVIPOLA'].values
logo = LeaveOneGroupOut()

def mae_top1(y, pred, g):
    mae = np.mean(np.abs(y - pred)) * 100
    r2  = 1 - np.sum((y-pred)**2) / np.sum((y-y.mean())**2)
    tmp = pd.DataFrame({'g': g, 'y': y, 'pred': pred})
    ac = tot = 0
    for _, s in tmp.groupby('g'):
        ac += int(s['y'].idxmax() == s['pred'].idxmax()); tot += 1
    return mae, r2, 100*ac/tot

def normalize_within(pred, groups):
    """Normalizar predicciones dentro de cada contienda para sumar 1."""
    out = pred.copy()
    for grp in np.unique(groups):
        mask = groups == grp
        s = out[mask].sum()
        if s > 0: out[mask] /= s
    return out

print("="*65)
print("  DIAGNÓSTICO: Comparación de implementaciones LOCO-CV")
print("="*65)

# ── Modelo A: GLM sin normalizar (el de verificar_replicabilidad.py) ──────────
print("\n[A] GLM binomial + StandardScaler, SIN normalizar")
pred_A = np.full(len(y), np.nan)
for tr, te in logo.split(X, y, g):
    sc = StandardScaler().fit(X[tr])
    Xtr = sm.add_constant(sc.transform(X[tr]))
    Xte = sm.add_constant(sc.transform(X[te]), has_constant='add')
    try:
        m = sm.GLM(y[tr], Xtr, family=sm.families.Binomial()).fit()
        pred_A[te] = m.predict(Xte)
    except: pred_A[te] = y[tr].mean()
mae_A, r2_A, top1_A = mae_top1(y, pred_A, g)
print(f"    MAE={mae_A:.2f} pp | R²={r2_A:.3f} | Top-1={top1_A:.1f}%")

# ── Modelo B: GLM binomial + StandardScaler, CON normalizar ───────────────────
print("\n[B] GLM binomial + StandardScaler, CON normalizar dentro de contienda")
pred_B = normalize_within(pred_A, g)
mae_B, r2_B, top1_B = mae_top1(y, pred_B, g)
print(f"    MAE={mae_B:.2f} pp | R²={r2_B:.3f} | Top-1={top1_B:.1f}%")

# ── Modelo C: OLS en logit(y), sin scaler, CON normalizar (= script figuras) ──
print("\n[C] OLS sobre logit(y), SIN StandardScaler, CON normalizar  [= generar_figuras]")
pred_C = np.full(len(y), np.nan)
for tr, te in logo.split(X, y, g):
    X_tr, X_te = X[tr], X[te]
    y_tr, y_te = y[tr], y[te]
    logit_y = np.log(np.clip(y_tr,1e-4,1-1e-4)/(1-np.clip(y_tr,1e-4,1-1e-4)))
    Xc_tr = np.column_stack([np.ones(len(X_tr)), X_tr])
    Xc_te = np.column_stack([np.ones(len(X_te)), X_te])
    try:
        coef, *_ = np.linalg.lstsq(Xc_tr, logit_y, rcond=None)
        raw = special.expit(Xc_te @ coef)
        s = raw.sum()
        if s > 0: raw /= s
        pred_C[te] = raw
    except: pred_C[te] = 1/len(te)
mae_C, r2_C, top1_C = mae_top1(y, pred_C, g)
print(f"    MAE={mae_C:.2f} pp | R²={r2_C:.3f} | Top-1={top1_C:.1f}%")

# ── Modelo D: OLS en logit(y), SIN normalizar ─────────────────────────────────
print("\n[D] OLS sobre logit(y), SIN normalizar")
pred_D = np.full(len(y), np.nan)
for tr, te in logo.split(X, y, g):
    X_tr, X_te = X[tr], X[te]
    y_tr = y[tr]
    logit_y = np.log(np.clip(y_tr,1e-4,1-1e-4)/(1-np.clip(y_tr,1e-4,1-1e-4)))
    Xc_tr = np.column_stack([np.ones(len(X_tr)), X_tr])
    Xc_te = np.column_stack([np.ones(len(X_te)), X_te])
    try:
        coef, *_ = np.linalg.lstsq(Xc_tr, logit_y, rcond=None)
        pred_D[te] = special.expit(Xc_te @ coef)
    except: pred_D[te] = 1/len(te)
mae_D, r2_D, top1_D = mae_top1(y, pred_D, g)
print(f"    MAE={mae_D:.2f} pp | R²={r2_D:.3f} | Top-1={top1_D:.1f}%")

# ── Modelo E: GLM sin scaler, con normalizar ───────────────────────────────────
print("\n[E] GLM binomial, SIN StandardScaler, CON normalizar")
pred_E = np.full(len(y), np.nan)
for tr, te in logo.split(X, y, g):
    Xtr = sm.add_constant(X[tr])
    Xte = sm.add_constant(X[te], has_constant='add')
    try:
        m = sm.GLM(y[tr], Xtr, family=sm.families.Binomial()).fit()
        raw = m.predict(Xte)
        s = raw.sum()
        if s > 0: raw /= s
        pred_E[te] = raw
    except: pred_E[te] = y[tr].mean()
mae_E, r2_E, top1_E = mae_top1(y, pred_E, g)
print(f"    MAE={mae_E:.2f} pp | R²={r2_E:.3f} | Top-1={top1_E:.1f}%")

print("\n" + "="*65)
print("  TABLA COMPARATIVA")
print("="*65)
print(f"  {'Modelo':<50} {'MAE':>6}  {'R²':>6}  {'Top1':>6}")
print(f"  {'-'*50} {'-'*6}  {'-'*6}  {'-'*6}")
for nombre, mae, r2, top1 in [
    ("A: GLM + scaler, sin normalizar (notebook original)",  mae_A, r2_A, top1_A),
    ("B: GLM + scaler, CON normalizar",                      mae_B, r2_B, top1_B),
    ("C: OLS-logit, sin scaler, CON normalizar (figuras)",   mae_C, r2_C, top1_C),
    ("D: OLS-logit, sin scaler, sin normalizar",             mae_D, r2_D, top1_D),
    ("E: GLM sin scaler, CON normalizar",                    mae_E, r2_E, top1_E),
]:
    print(f"  {nombre:<50} {mae:>6.2f}  {r2:>6.3f}  {top1:>5.1f}%")
print("="*65)

best = min([(mae_A,'A'),(mae_B,'B'),(mae_C,'C'),(mae_D,'D'),(mae_E,'E')], key=lambda x: x[0])
print(f"\n  ► MEJOR MAE: Modelo {best[1]} ({best[0]:.2f} pp)")
print(f"\n  ► La diferencia entre normalizar y no normalizar (A vs B): {abs(mae_A-mae_B):.2f} pp")
print(f"  ► La diferencia entre GLM y OLS-logit (B vs C): {abs(mae_B-mae_C):.2f} pp")
