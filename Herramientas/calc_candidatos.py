import pandas as pd
import numpy as np

df = pd.read_csv(r'c:\Users\juans\Downloads\Avances_tesis\Herramientas\resultados\redes_unificadas.csv', sep=';', encoding='utf-8-sig')
df_electoral = pd.read_excel(r'c:\Users\juans\Downloads\Avances_tesis\Colombia\Resultados electorales.xlsx', sheet_name='Candidatos E-26 ALC')
df_electoral = df_electoral.rename(columns={'ID Candidato': 'id_candidato'})

# Excluir los mismos dos municipios que el modelo
for ex in ['68547', '68081']:
    df = df[~df['id_candidato'].str.contains(ex, na=False)]

df['DIVIPOLA'] = df['id_candidato'].astype(str).str.split('-').str[1].str.zfill(5)
df_m = df.merge(df_electoral[['id_candidato','Votos']], on='id_candidato', how='left')
df_valid = df_m[df_m['Votos'] >= 10000].drop_duplicates('id_candidato')

cands_per = df_valid.groupby('DIVIPOLA')['id_candidato'].count()
promedio = cands_per.mean()

print(f"Contiendas: {len(cands_per)}")
print(f"Candidatos totales (>10k votos): {df_valid['id_candidato'].nunique()}")
print(f"Candidatos promedio por contienda: {promedio:.4f}")
print(f"1 / promedio = {1/promedio*100:.2f}%  (azar puro)")
print()
print("Distribucion de candidatos por contienda:")
print(cands_per.value_counts().sort_index())
