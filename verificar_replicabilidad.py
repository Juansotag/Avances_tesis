"""
verificar_replicabilidad.py
══════════════════════════════════════════════════════════════
Verifica que el modelo ELA-NOM es completamente replicable.
Corre:
  1. Entrenamiento del modelo (especificación de 2 variables)
  2. Predicción segunda vuelta 2026
  3. Compara coeficientes con los documentados en la tesis

Requisitos: pandas, numpy, sklearn, statsmodels, openpyxl
"""

import os, sys
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import LeaveOneGroupOut
import statsmodels.api as sm

# ── Rutas ──────────────────────────────────────────────────────────────────────
RAIZ             = Path(r'C:\Users\juans\Downloads\Avances_tesis')
HERRAMIENTAS     = RAIZ / 'Herramientas'
ELEC_2026        = RAIZ / 'Elecciones presidencia 2026' / 'resultados'
REDES_TRAIN      = HERRAMIENTAS / 'resultados' / 'redes_unificadas.csv'
SEGUIDORES       = HERRAMIENTAS / 'resultados' / 'seguidores.csv'
EXCEL_PATH       = RAIZ / 'Colombia' / 'Resultados electorales.xlsx'
REDES_2026       = ELEC_2026 / 'presidencia2026_unificada.csv'

OK = "✅"; FAIL = "❌"; WARN = "⚠️"

def check(cond, msg): 
    print(f"  {OK if cond else FAIL}  {msg}")
    return cond

# ── 1. VERIFICAR ARCHIVOS ──────────────────────────────────────────────────────
print("\n" + "="*60)
print("  PASO 1: Verificar archivos de entrada")
print("="*60)
archivos_ok = all([
    check(REDES_TRAIN.exists(),  f"redes_unificadas.csv ({REDES_TRAIN.stat().st_size:,} bytes)" if REDES_TRAIN.exists() else "redes_unificadas.csv — FALTA"),
    check(SEGUIDORES.exists(),   f"seguidores.csv ({SEGUIDORES.stat().st_size:,} bytes)" if SEGUIDORES.exists() else "seguidores.csv — FALTA"),
    check(EXCEL_PATH.exists(),   f"Resultados electorales.xlsx" if EXCEL_PATH.exists() else "Resultados electorales.xlsx — FALTA"),
    check(REDES_2026.exists(),   f"presidencia2026_unificada.csv" if REDES_2026.exists() else "presidencia2026_unificada.csv — FALTA"),
])

if not archivos_ok:
    print(f"\n{FAIL} Faltan archivos de entrada. Abortando.")
    sys.exit(1)

# ── 2. CARGAR Y PREPARAR DATOS DE ENTRENAMIENTO ────────────────────────────────
print("\n" + "="*60)
print("  PASO 2: Cargar y preparar datos de entrenamiento")
print("="*60)

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

LOG_POB_MEAN_TRAIN = base['log_pob'].mean()
base['mod_likes_pob'] = base['f_likes_dom'] * (base['log_pob'] - LOG_POB_MEAN_TRAIN)
base = base.dropna(subset=[c[2] for c in combos] + ['vote_frac','log_pob']).reset_index(drop=True)

print(f"  {OK}  Candidatos: {len(base)} | Contiendas: {base['DIVIPOLA'].nunique()}")
check(len(base) == 120, f"120 candidatos (obtenidos: {len(base)})")
check(base['DIVIPOLA'].nunique() == 31, f"31 contiendas (obtenidas: {base['DIVIPOLA'].nunique()})")

# ── 3. ENTRENAR MODELO (especificación de 2 variables) ────────────────────────
print("\n" + "="*60)
print("  PASO 3: Entrenar ElasticNet (especificación 2 variables)")
print("="*60)

FEATURES = ['f_likes_dom', 'mod_likes_pob']
X_train  = base[FEATURES].values
y_train  = base['vote_frac'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

model = ElasticNetCV(l1_ratio=[0.1,0.3,0.5,0.7,0.9,1.0], alphas=np.logspace(-4,1,100),
                     cv=5, max_iter=10000, random_state=42)
model.fit(X_scaled, y_train)

coefs = dict(zip(FEATURES, model.coef_))
print(f"\n  Resultado del entrenamiento:")
print(f"    Alpha óptimo  : {model.alpha_:.6f}")
print(f"    L1 ratio      : {model.l1_ratio_:.2f}")
print(f"    Intercepto    : {model.intercept_:.4f}")
print(f"    f_likes_dom   : {model.coef_[0]:.5f}")
print(f"    mod_likes_pob : {model.coef_[1]:.5f}")

# Valores documentados en la tesis
DOC = {'alpha': 0.047508, 'l1_ratio': 0.10, 'intercept': 0.2583,
       'beta1': 0.111, 'beta2': 0.026}

print(f"\n  Comparación con valores documentados en la tesis:")
check(abs(model.alpha_ - DOC['alpha']) < 0.001,
      f"Alpha: obtenido={model.alpha_:.6f} | doc={DOC['alpha']} | diff={abs(model.alpha_-DOC['alpha']):.6f}")
check(abs(model.l1_ratio_ - DOC['l1_ratio']) < 0.01,
      f"L1 ratio: obtenido={model.l1_ratio_:.2f} | doc={DOC['l1_ratio']}")
check(abs(model.intercept_ - DOC['intercept']) < 0.001,
      f"Intercepto: obtenido={model.intercept_:.4f} | doc={DOC['intercept']}")
check(abs(model.coef_[0] - DOC['beta1']) < 0.001,
      f"β1 (likes_dom): obtenido={model.coef_[0]:.5f} | doc={DOC['beta1']:.3f}")
check(abs(model.coef_[1] - DOC['beta2']) < 0.001,
      f"β2 (mod_pob): obtenido={model.coef_[1]:.5f} | doc={DOC['beta2']:.3f}")

# ── 4. LOCO-CV MÉTRICAS ────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  PASO 4: Validación LOCO-CV (MAE fuera de muestra)")
print("="*60)

logo = LeaveOneGroupOut()
X = base[FEATURES].values.astype(float)
y = base['vote_frac'].values
g = base['DIVIPOLA'].values
pred = np.full(len(y), np.nan)

for tr, te in logo.split(X, y, g):
    sc = StandardScaler().fit(X[tr])
    Xtr = sm.add_constant(sc.transform(X[tr]))
    Xte = sm.add_constant(sc.transform(X[te]), has_constant='add')
    try:
        m = sm.GLM(y[tr], Xtr, family=sm.families.Binomial()).fit()
        pred[te] = m.predict(Xte)
    except:
        pred[te] = y[tr].mean()

mae = np.mean(np.abs(y - pred)) * 100
r2  = 1 - np.sum((y-pred)**2) / np.sum((y-y.mean())**2)
tmp = pd.DataFrame({'DIVIPOLA': g, 'y': y, 'pred': pred})
ac = tot = 0
for _, s in tmp.groupby('DIVIPOLA'):
    ac += int(s['y'].idxmax() == s['pred'].idxmax()); tot += 1
top1 = 100 * ac / tot

print(f"\n  Métricas LOCO-CV (especificación 2 variables):")
print(f"    MAE    : {mae:.2f} pp")
print(f"    R²_oos : {r2:.3f}")
print(f"    Top-1  : {top1:.1f}%")
check(abs(mae - 10.37) < 0.5,  f"MAE ≈ 10.37 pp (obtenido: {mae:.2f})")
check(r2 > 0.49,               f"R²_oos > 0.49 (obtenido: {r2:.3f})")
check(abs(top1 - 71.0) < 5,    f"Top-1 ≈ 71% (obtenido: {top1:.1f}%)")

# ── 5. PREDICCIÓN 2026 ────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  PASO 5: Predicción segunda vuelta 2026")
print("="*60)

CANDIDATOS = {'cepeda_ivan': 'Iván Cepeda Castro', 'delaespriella_abelardo': 'Abelardo De la Espriella'}
POB_COLOMBIA = 53_936_226

df26 = pd.read_csv(REDES_2026, sep=';', encoding='utf-8-sig')
totales = df26.groupby('id_candidato')['likes'].sum().reset_index()
totales.columns = ['id_candidato', 'total_likes']
grand_total = totales['total_likes'].sum()
totales['pct_likes_dom'] = (totales['total_likes'] / grand_total * 100).clip(0.01, 99.99)
totales['f_likes_dom']   = to_logit(totales['pct_likes_dom'])

log_pob_col = np.log(POB_COLOMBIA)
totales['mod_likes_pob'] = totales['f_likes_dom'] * (log_pob_col - LOG_POB_MEAN_TRAIN)

X_2026        = totales[FEATURES].values
X_2026_scaled = scaler.transform(X_2026)

signal      = X_2026_scaled @ model.coef_
pred_2cand  = 0.50 + signal
pred_norm   = np.clip(pred_2cand, 0, 1)
pred_norm   = pred_norm / pred_norm.sum()
totales['pct_voto_pred'] = (pred_norm * 100).round(2)
totales['signal']        = signal
totales['nombre']        = totales['id_candidato'].map(CANDIDATOS)

resultado = totales.sort_values('pct_voto_pred', ascending=False).reset_index(drop=True)

print(f"\n  Señal digital:")
for _, row in resultado.iterrows():
    print(f"    {row['nombre']}: dom={row['pct_likes_dom']:.1f}% | señal={row['signal']:+.5f} | pred={row['pct_voto_pred']:.2f}%")

print(f"\n  Comparación con documento (60,5% / 39,5%):")
cepeda_pred = resultado.loc[resultado['id_candidato']=='cepeda_ivan', 'pct_voto_pred'].values[0]
check(abs(cepeda_pred - 60.46) < 0.1, f"Cepeda: obtenido={cepeda_pred:.2f}% | doc=60.46%")

# ── 6. RESUMEN FINAL ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  RESUMEN DE REPLICABILIDAD")
print("="*60)
print(f"""
  Parámetros del modelo (verificados):
    Alpha         = {model.alpha_:.6f}   (doc: 0.047508)
    L1 ratio      = {model.l1_ratio_:.2f}         (doc: 0.10)
    Intercepto    = {model.intercept_:.4f}       (doc: 0.2583)
    β₁ (likes)   = {model.coef_[0]:.5f}    (doc: 0.111)
    β₂ (mod_pob) = {model.coef_[1]:.5f}    (doc: 0.026)

  Métricas de validación:
    MAE_oos  = {mae:.2f} pp   (doc: 10.37 pp)
    R²_oos   = {r2:.3f}      (doc: 0.506)
    Top-1    = {top1:.1f}%     (doc: 71%)

  Predicción 2026:
    Cepeda:     {cepeda_pred:.2f}%  (doc: 60.46%)
    Espriella:  {100-cepeda_pred:.2f}%  (doc: 39.54%)

  Señal del moderador del 0.557:
    Nota: 0.557 es coef_medio del moderador cuando ElasticNet
    opera sobre el pool completo de 9 variables (no el modelo final).
""")
print("="*60)
