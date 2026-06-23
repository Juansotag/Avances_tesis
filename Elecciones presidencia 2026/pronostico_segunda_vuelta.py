"""
pronostico_segunda_vuelta.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pronóstico corregido para la SEGUNDA VUELTA presidencial (2 candidatos).

Corrección clave vs. versión anterior:
- El modelo ElasticNet fue entrenado en contiendas multi-candidato
  (intercepto ≈ 0.26, no 0.50).
- Para una contienda de exactamente 2 candidatos, la línea base natural
  es 50/50 → eliminamos el intercepto multi-candidato y re-centramos en 0.50.
- Población de Colombia actualizada a 53,936,226.

Uso:
    python pronostico_segunda_vuelta.py
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV

# ── Rutas ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR       = Path(os.path.abspath(__file__)).parent
RAIZ_DIR         = SCRIPT_DIR.parent
HERRAMIENTAS_DIR = RAIZ_DIR / 'Herramientas'
RESULTADOS_DIR   = SCRIPT_DIR / 'resultados'

REDES_TRAIN   = HERRAMIENTAS_DIR / 'resultados' / 'redes_unificadas.csv'
REDES_2026    = RESULTADOS_DIR / 'presidencia2026_unificada.csv'
SEGUIDORES    = HERRAMIENTAS_DIR / 'resultados' / 'seguidores.csv'
EXCEL_PATH    = RAIZ_DIR / 'Colombia' / 'Resultados electorales.xlsx'

# ── Candidatos ──────────────────────────────────────────────────────────────────
CANDIDATOS = {
    'cepeda_ivan':            'Iván Cepeda Castro',
    'delaespriella_abelardo': 'Abelardo De la Espriella',
}
POB_COLOMBIA = 53_936_226  # dato del usuario

# ── Helpers (idénticos al notebook 03_automl_seleccion) ───────────────────────
def to_logit(p_pct, eps=1e-3):
    p = np.clip(p_pct / 100, eps, 1 - eps)
    return np.log(p / (1 - p))


def prepare_lens_data(data, metric_col, lente='dominancia'):
    data = data.copy()
    if len(data) == 0 or metric_col not in data.columns:
        return pd.DataFrame()
    agg = data.groupby(['DIVIPOLA', 'id_candidato', 'Candidato', 'Ganador']).agg(
        metric_sum=(metric_col, 'sum'),
        n_posts=(metric_col, 'count'),
        votos=('Votos', 'first'),
        pob=('Población 2023', 'first')
    ).reset_index()
    if lente in ('totales', 'dominancia'):
        agg['v'] = agg['metric_sum']
    elif lente == 'por_post':
        agg['v'] = agg['metric_sum'] / agg['n_posts'].replace(0, np.nan)
    agg = agg.replace([np.inf, -np.inf], np.nan)
    agg['pct_metric'] = (agg['v'] / agg.groupby('DIVIPOLA')['v'].transform('sum')) * 100
    return agg[agg.groupby('DIVIPOLA')['v'].transform('sum') > 0]


# ── 1. Datos de entrenamiento ──────────────────────────────────────────────────
print('\n📚 Cargando datos de entrenamiento (elecciones municipales 2023)...')
df_redes      = pd.read_csv(REDES_TRAIN,  sep=';', encoding='utf-8-sig')
df_electoral  = pd.read_excel(EXCEL_PATH, sheet_name='Candidatos E-26 ALC').rename(
                    columns={'ID Candidato': 'id_candidato'})
df_poblacion  = pd.read_excel(EXCEL_PATH, sheet_name='Población 2023 (DANE)')
df_seguidores = pd.read_csv(SEGUIDORES,   sep=';', encoding='utf-8-sig').fillna(0)

for ex in ['68547', '68081']:
    df_redes = df_redes[~df_redes['id_candidato'].str.contains(ex, na=False)]

df = df_redes.merge(
        df_seguidores[['id_candidato','tiktok_followers','twitter_followers','facebook_followers']],
        on='id_candidato', how='left')
df = df.merge(
        df_electoral[['id_candidato','Candidato','Ganador','Votos']],
        on='id_candidato', how='left')
df['DIVIPOLA'] = df['id_candidato'].astype(str).str.split('-').str[1].str.zfill(5)
df_poblacion['DIVIPOLA'] = (
    pd.to_numeric(df_poblacion['DIVIPOLA'], errors='coerce')
      .fillna(0).astype(int).astype(str).str.zfill(5)
)
df = df.merge(df_poblacion[['DIVIPOLA','Población 2023']], on='DIVIPOLA', how='left')
print(f'   Candidatos: {df["id_candidato"].nunique()} | Contiendas: {df["DIVIPOLA"].nunique()}')

# ── 2. Feature engineering (igual al modelo original) ─────────────────────────
combos = [
    ('likes',      'dominancia', 'f_likes_dom'),
    ('comentarios','dominancia', 'f_coment_dom'),
    ('compartidos','dominancia', 'f_compart_dom'),
    ('likes',      'por_post',   'f_likes_pp'),
    ('comentarios','por_post',   'f_coment_pp'),
    ('compartidos','por_post',   'f_compart_pp'),
]

b = prepare_lens_data(df, 'likes', 'dominancia')
b['total_votos'] = b.groupby('DIVIPOLA')['votos'].transform('sum')
b['vote_frac']   = (b['votos'] / b['total_votos']).clip(1e-4, 1 - 1e-4)
b['n_candidatos']= b.groupby('DIVIPOLA')['id_candidato'].transform('count')
b['log_pob']     = np.log(b['pob'].clip(lower=1))
base = b[['id_candidato','DIVIPOLA','Candidato','Ganador','vote_frac','n_candidatos','log_pob']].copy()

for tipo, lente, nombre in combos:
    d = prepare_lens_data(df, tipo, lente)[['id_candidato','pct_metric']]
    base = base.merge(d.rename(columns={'pct_metric': nombre}), on='id_candidato', how='left')

for nombre in [c[2] for c in combos]:
    base[nombre] = to_logit(base[nombre])

LOG_POB_MEAN_TRAIN = base['log_pob'].mean()
base['mod_likes_pob'] = base['f_likes_dom'] * (base['log_pob'] - LOG_POB_MEAN_TRAIN)
base = base.dropna(subset=[c[2] for c in combos] + ['vote_frac', 'log_pob']).reset_index(drop=True)

# ── 3. Entrenar ElasticNet (especificación ganadora: likes + moderador_pob) ───
print('\n🤖 Entrenando ElasticNet (especificación ganadora)...')
FEATURES = ['f_likes_dom', 'mod_likes_pob']
X_train = base[FEATURES].values
y_train = base['vote_frac'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

model = ElasticNetCV(
    l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
    alphas=np.logspace(-4, 1, 100),
    cv=5, max_iter=10000, random_state=42
)
model.fit(X_scaled, y_train)

intercepto = model.intercept_
n_cand_medio_train = base.groupby('DIVIPOLA')['id_candidato'].count().mean()
print(f'   Intercepto (multi-cand): {intercepto:.4f}')
print(f'   Nº candidatos medio (entrenamiento): {n_cand_medio_train:.1f}')
print(f'   Coeficientes: {dict(zip(FEATURES, model.coef_))}')

# ── 4. Features para los candidatos 2026 ──────────────────────────────────────
print('\n📊 Calculando features de los candidatos presidenciales...')
df26 = pd.read_csv(REDES_2026, sep=';', encoding='utf-8-sig')

totales = df26.groupby('id_candidato')['likes'].sum().reset_index()
totales.columns = ['id_candidato', 'total_likes']
grand_total = totales['total_likes'].sum()
totales['pct_likes_dom'] = (totales['total_likes'] / grand_total * 100).clip(0.01, 99.99)
totales['f_likes_dom']   = to_logit(totales['pct_likes_dom'])

log_pob_col = np.log(POB_COLOMBIA)
totales['mod_likes_pob'] = totales['f_likes_dom'] * (log_pob_col - LOG_POB_MEAN_TRAIN)
totales['nombre'] = totales['id_candidato'].map(CANDIDATOS)

# ── 5. Predicción — RE-CENTRADO PARA 2 CANDIDATOS ─────────────────────────────
print('\n🔮 Generando pronóstico (re-centrado para 2 candidatos)...')

X_2026 = totales[FEATURES].values
X_2026_scaled = scaler.transform(X_2026)

#
# CORRECCIÓN CLAVE:
# El modelo fue entrenado en contiendas con múltiples candidatos, por eso
# su intercepto ≈ 0.26 (≈ cuota media en una contienda de 4 candidatos).
# Para una segunda vuelta de EXACTAMENTE 2 candidatos, la línea base es 50/50.
# Solución: usar solo la SEÑAL (beta × X) sin el intercepto, y re-centrar en 0.50.
#
signal = X_2026_scaled @ model.coef_   # contribución pura de features (sin intercepto)
pred_2cand = 0.50 + signal             # re-centrado en 0.50

# Normalizar (para asegurar que sumen exactamente 1)
pred_norm = np.clip(pred_2cand, 0, 1)
pred_norm = pred_norm / pred_norm.sum()

totales['signal']        = signal
totales['pred_raw']      = 0.50 + signal
totales['pct_voto_pred'] = (pred_norm * 100).round(2)

resultado = totales.sort_values('pct_voto_pred', ascending=False).reset_index(drop=True)

# ── 6. Imprimir resultado ──────────────────────────────────────────────────────
sep = '=' * 62
print(f'\n{sep}')
print(f'  PRONÓSTICO — SEGUNDA VUELTA PRESIDENCIAL COLOMBIA 2026')
print(f'  Fecha: 21 de junio de 2026')
print(f'{sep}')
print(f'  Población Colombia         : {POB_COLOMBIA:,}')
print(f'  Intercepto entrenamiento   : {intercepto:.4f} (multi-cand, NO aplica aquí)')
print(f'  Línea base usada           : 0.50 (contienda de 2 candidatos)')
print(f'{sep}')

for _, row in resultado.iterrows():
    print(f"\n  👤 {row['nombre']}")
    print(f"     Likes totales          : {int(row['total_likes']):,}")
    print(f"     Dominancia likes       : {row['pct_likes_dom']:.1f}%")
    print(f"     Señal digital (logit)  : {row['signal']:+.4f}")
    print(f"     ► Pronóstico           : {row['pct_voto_pred']:.1f}%")

print(f'\n{sep}')
winner = resultado.iloc[0]
print(f"  🏆 Favorito: {winner['nombre']} ({winner['pct_voto_pred']:.1f}%)")
print(f'  ⚠️  MAE del modelo en CV: ~10 pp → rango: [{winner["pct_voto_pred"]-10:.0f}% – {min(100, winner["pct_voto_pred"]+10):.0f}%]')
print(f'{sep}\n')

# ── 7. Guardar ─────────────────────────────────────────────────────────────────
out = RESULTADOS_DIR / 'presidencia2026_pronostico_v2.csv'
resultado[['id_candidato','nombre','total_likes','pct_likes_dom',
           'signal','pct_voto_pred']].to_csv(out, index=False, sep=';', encoding='utf-8-sig')
print(f'💾 Resultados guardados en: {out}')
