"""
Descomposicion del rho de Spearman: componente composicional vs. senal real
============================================================================
Metodo: permutacion de likes dentro de cada contienda (10.000 iteraciones).
En cada iteracion se reasignan aleatoriamente los likes entre candidatos
dentro de cada ciudad, preservando el total de likes por ciudad.
El rho nulo promedio = componente puramente composicional.
La diferencia rho_observado - rho_nulo_medio = componente de senal real.
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
N = 10_000

# ─────────────────────────────────────────────────────────────────
# 1. Carga de datos (mismo pipeline que permutation_test.py)
# ─────────────────────────────────────────────────────────────────
DATA_POST = r"c:\Users\juans\Downloads\Avances_tesis\Herramientas\resultados\redes_unificadas_descontadas.csv"
RESULTS   = r"c:\Users\juans\Downloads\Avances_tesis\Colombia\Resultados electorales.xlsx"

df_posts = pd.read_csv(DATA_POST, sep=';', encoding='utf-8-sig', low_memory=False)
df_res   = pd.read_excel(RESULTS)

df_res.columns = df_res.columns.str.strip()
df_res = df_res.rename(columns={
    'ID Candidato': 'id_candidato',
    'Votos': 'votos',
    'Ganador': 'ganador',
    'DIVIPOLA': 'divipola'
})
df_res['id_candidato'] = df_res['id_candidato'].astype(str).str.strip()
df_res = df_res[df_res['votos'] >= 10_000].copy()

# Likes totales por candidato
df_posts['id_candidato'] = df_posts['id_candidato'].astype(str).str.strip()
likes_cand = (
    df_posts.groupby('id_candidato')['likes']
    .apply(lambda x: pd.to_numeric(x, errors='coerce').sum())
    .reset_index()
    .rename(columns={'likes': 'total_likes'})
)

df = df_res.merge(likes_cand, on='id_candidato', how='left')
df['total_likes'] = df['total_likes'].fillna(0)

# Cuota de votos por candidato
votos_ciudad = df.groupby('divipola')['votos'].sum().reset_index().rename(columns={'votos': 'votos_ciudad'})
df = df.merge(votos_ciudad, on='divipola', how='left')
df['cuota_votos'] = df['votos'] / df['votos_ciudad']

# Dominancia de likes
likes_ciudad = df.groupby('divipola')['total_likes'].sum().reset_index().rename(columns={'total_likes': 'likes_ciudad'})
df = df.merge(likes_ciudad, on='divipola', how='left')
df['dominancia_likes'] = np.where(df['likes_ciudad'] > 0,
                                   df['total_likes'] / df['likes_ciudad'], 0)

# Solo candidatos con publicaciones
df_con = df[df['total_likes'] > 0].copy()
print(f"Candidatos con publicaciones: {len(df_con)}")

# ─────────────────────────────────────────────────────────────────
# 2. rho observado
# ─────────────────────────────────────────────────────────────────
rho_obs, p_obs = stats.spearmanr(df_con['dominancia_likes'], df_con['cuota_votos'])
print(f"\nrho observado: {rho_obs:.4f} (p = {p_obs:.2e})")

# ─────────────────────────────────────────────────────────────────
# 3. Permutacion de likes DENTRO de cada ciudad (10.000 iteraciones)
#    Preserva la estructura composicional pero elimina la senal real
# ─────────────────────────────────────────────────────────────────
print(f"\nPermutando likes dentro de cada ciudad ({N:,} iteraciones)...")

ciudades = df_con['divipola'].unique()
rho_nulos = np.zeros(N)

for i in range(N):
    df_perm = df_con.copy()
    for ciudad in ciudades:
        mask = df_perm['divipola'] == ciudad
        idx = df_perm.index[mask]
        if len(idx) <= 1:
            continue
        # Barajar los likes dentro de la ciudad
        likes_orig = df_perm.loc[idx, 'total_likes'].values.copy()
        np.random.shuffle(likes_orig)
        df_perm.loc[idx, 'total_likes'] = likes_orig

    # Recalcular dominancia con likes barajados
    total_por_ciudad = df_perm.groupby('divipola')['total_likes'].transform('sum')
    dom_perm = np.where(total_por_ciudad > 0,
                        df_perm['total_likes'] / total_por_ciudad, 0)

    rho_nulos[i], _ = stats.spearmanr(dom_perm, df_perm['cuota_votos'])

# ─────────────────────────────────────────────────────────────────
# 4. Resultados
# ─────────────────────────────────────────────────────────────────
rho_nulo_medio   = rho_nulos.mean()
rho_nulo_p95     = np.percentile(rho_nulos, 95)
rho_senal        = rho_obs - rho_nulo_medio
pct_composicional = (rho_nulo_medio / rho_obs) * 100
pct_senal         = (rho_senal / rho_obs) * 100
p_val_nulo = (rho_nulos >= rho_obs).mean()

print("\n" + "="*60)
print("DESCOMPOSICION DE rho = 0.70")
print("="*60)
print(f"rho observado:                     {rho_obs:.4f}")
print(f"rho nulo medio (composicional):    {rho_nulo_medio:.4f}  ({pct_composicional:.1f}% del rho total)")
print(f"rho de senal real:                 {rho_senal:.4f}  ({pct_senal:.1f}% del rho total)")
print(f"")
print(f"Percentil 95 del nulo:             {rho_nulo_p95:.4f}")
print(f"p-valor (rho_obs >= distribucion nula): {p_val_nulo:.4f}")
print(f"")
print(f"Distribucion nula:")
print(f"  Media:  {rho_nulo_medio:.4f}")
print(f"  Desv.:  {rho_nulos.std():.4f}")
print(f"  Min:    {rho_nulos.min():.4f}")
print(f"  Max:    {rho_nulos.max():.4f}")
print("="*60)
print(f"\nCONCLUSION:")
print(f"De rho = {rho_obs:.3f}, aprox. {rho_nulo_medio:.3f} es composicional")
print(f"y aprox. {rho_senal:.3f} es senal predictiva real.")
print(f"El {pct_senal:.0f}% del rho corresponde a senal genuina.")
