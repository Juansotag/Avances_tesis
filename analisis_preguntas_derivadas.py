import pandas as pd
import numpy as np
import scipy.special as sp
from scipy import stats
import matplotlib.pyplot as plt
import json

# Cargar dataset
df = pd.read_csv('Herramientas/ipynb antiguo/dataset_modelo_electoral.csv')

# 1. Calcular cuota real de votos por municipio
df['total_votos_muni'] = df.groupby('Municipio')['Votos'].transform('sum')
df['cuota_votos_real'] = df['Votos'] / df['total_votos_muni']

# 2. Calcular dominancia de likes por municipio
df['total_likes_muni'] = df.groupby('Municipio')['total_likes'].transform('sum')
df['dominancia_likes'] = np.where(df['total_likes_muni'] > 0, df['total_likes'] / df['total_likes_muni'], 0)

# Imputacion segura de dominancia en logit
eps = 1e-4
df['logit_likes'] = sp.logit(np.clip(df['dominancia_likes'], eps, 1 - eps))

# 3. Traccion tardia combinada
df['total_late_growth'] = df['facebook_likes_late_growth'].fillna(0) + df['tiktok_likes_late_growth'].fillna(0) + df['twitter_likes_late_growth'].fillna(0)
df['total_late_muni'] = df.groupby('Municipio')['total_late_growth'].transform('sum')
df['dominancia_late'] = np.where(df['total_late_muni'] > 0, df['total_late_growth'] / df['total_late_muni'], 0)

municipios = df['Municipio'].unique()
n_municipios = len(municipios)
print(f"Total municipios: {n_municipios}, Total candidatos: {len(df)}")

# --- EXPERIMENTO 1: Curva de Aprendizaje (Pregunta Derivada 4) ---
sample_sizes = [5, 10, 15, 20, 25, 30]
n_repit = 50
learning_results = []

np.random.seed(42)

for size in sample_sizes:
    maes_size = []
    for _ in range(n_repit):
        train_munis = np.random.choice(municipios, size=size, replace=False)
        test_munis = [m for m in municipios if m not in train_munis]
        if len(test_munis) == 0:
            test_munis = train_munis
        
        train_df = df[df['Municipio'].isin(train_munis)]
        test_df = df[df['Municipio'].isin(test_munis)]
        
        slope, intercept = np.polyfit(train_df['logit_likes'], train_df['cuota_votos_real'], 1)
        preds = np.clip(slope * test_df['logit_likes'] + intercept, 0, 1)
        mae = np.mean(np.abs(preds - test_df['cuota_votos_real'])) * 100
        maes_size.append(mae)
    
    mean_mae = np.mean(maes_size)
    std_mae = np.std(maes_size)
    learning_results.append({'sample_size': size, 'mean_mae': mean_mae, 'std_mae': std_mae})
    print(f"Tamaño de muestra (contiendas): {size:2d} -> MAE medio: {mean_mae:.2f}pp (+/- {std_mae:.2f}pp)")

df_learning = pd.DataFrame(learning_results)

# Graficar Curva de Aprendizaje
plt.figure(figsize=(8, 5))
plt.plot(df_learning['sample_size'], df_learning['mean_mae'], 'o-', color='#1f77b4', linewidth=2, markersize=8, label='MAE fuera de muestra')
plt.fill_between(df_learning['sample_size'], df_learning['mean_mae'] - df_learning['std_mae'], df_learning['mean_mae'] + df_learning['std_mae'], color='#1f77b4', alpha=0.2)
plt.title('Curva de Aprendizaje de ELA-NOM según el Número de Contiendas de Entrenamiento', fontsize=11, fontweight='bold')
plt.xlabel('Número de Contiendas en el Dataset de Entrenamiento', fontsize=10)
plt.ylabel('MAE en Puntos Porcentuales (pp)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('Manuscrito/tesis-sabana/img/col_learning_curve.png', dpi=300)
plt.close()
print("Grafico guardado en Manuscrito/tesis-sabana/img/col_learning_curve.png")

# --- EXPERIMENTO 2: Evaluacion de Traccion Tardia (Pregunta Derivada 3) ---
corr_total, _ = stats.spearmanr(df['dominancia_likes'], df['cuota_votos_real'])
corr_late, _ = stats.spearmanr(df['dominancia_late'], df['cuota_votos_real'])
print(f"\nSpearman Dominancia Total de Likes vs Votos: rho = {corr_total:.4f}")
print(f"Spearman Dominancia Traccion Tardia vs Votos: rho = {corr_late:.4f}")

# --- CREAR JUPYTER NOTEBOOK (.ipynb) EN FORMATO JSON DIRECTO ---
cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Análisis de Preguntas Derivadas 3 y 4 — ELA-NOM\n",
            "\n",
            "Este cuaderno operacionaliza y responde dos preguntas metodológicas planteadas por los jurados:\n",
            "\n",
            "1. **Pregunta Derivada 4 (Tamaño de Muestra y Curva de Aprendizaje):** ¿Cómo evoluciona el error (MAE) del modelo a medida que aumenta el número de contiendas históricas disponibles para entrenamiento?\n",
            "2. **Pregunta Derivada 3 (Tracción Tardía):** ¿Aporta la métrica de crecimiento de interacciones en los últimos días de campaña información predictiva adicional sobre la cuota final de voto?"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import numpy as np\n",
            "import scipy.special as sp\n",
            "import scipy.stats as stats\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "# Cargar dataset\n",
            "df = pd.read_csv('Herramientas/ipynb antiguo/dataset_modelo_electoral.csv')\n",
            "\n",
            "# Preprocesamiento\n",
            "df['total_votos_muni'] = df.groupby('Municipio')['Votos'].transform('sum')\n",
            "df['cuota_votos_real'] = df['Votos'] / df['total_votos_muni']\n",
            "df['total_likes_muni'] = df.groupby('Municipio')['total_likes'].transform('sum')\n",
            "df['dominancia_likes'] = np.where(df['total_likes_muni'] > 0, df['total_likes'] / df['total_likes_muni'], 0)\n",
            "\n",
            "print(f\"Total municipios: {df['Municipio'].nunique()}, Total candidatos: {len(df)}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Curva de Aprendizaje (Pregunta Derivada 4)\n",
            "\n",
            "Evaluación de la reducción del MAE fuera de muestra al variar el número de contiendas en el dataset de entrenamiento ($N \\in \\{5, 10, 15, 20, 25, 30\\}$)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "sample_sizes = [5, 10, 15, 20, 25, 30]\n",
            "n_repit = 50\n",
            "learning_results = []\n",
            "municipios = df['Municipio'].unique()\n",
            "\n",
            "np.random.seed(42)\n",
            "for size in sample_sizes:\n",
            "    maes_size = []\n",
            "    for _ in range(n_repit):\n",
            "        train_munis = np.random.choice(municipios, size=size, replace=False)\n",
            "        test_munis = [m for m in municipios if m not in train_munis]\n",
            "        if len(test_munis) == 0:\n",
            "            test_munis = train_munis\n",
            "        \n",
            "        train_df = df[df['Municipio'].isin(train_munis)]\n",
            "        test_df = df[df['Municipio'].isin(test_munis)]\n",
            "        \n",
            "        slope, intercept = np.polyfit(train_df['total_likes'], train_df['cuota_votos_real'], 1)\n",
            "        preds = np.clip(slope * test_df['total_likes'] + intercept, 0, 1)\n",
            "        mae = np.mean(np.abs(preds - test_df['cuota_votos_real'])) * 100\n",
            "        maes_size.append(mae)\n",
            "    \n",
            "    learning_results.append({'Contiendas_Entrenamiento': size, 'MAE_Medio_pp': np.mean(maes_size), 'Desv_Std': np.std(maes_size)})\n",
            "\n",
            "df_res = pd.DataFrame(learning_results)\n",
            "df_res"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Evaluación de Tracción Tardía (Pregunta Derivada 3)\n",
            "\n",
            "Comparación de la correlación de Spearman entre la dominancia acumulada total (14 días) y la dominancia restringida a la tracción tardía (últimos días de campaña)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "df['total_late_growth'] = df['facebook_likes_late_growth'].fillna(0) + df['tiktok_likes_late_growth'].fillna(0) + df['twitter_likes_late_growth'].fillna(0)\n",
            "df['total_late_muni'] = df.groupby('Municipio')['total_late_growth'].transform('sum')\n",
            "df['dominancia_late'] = np.where(df['total_late_muni'] > 0, df['total_late_growth'] / df['total_late_muni'], 0)\n",
            "\n",
            "rho_total, _ = stats.spearmanr(df['dominancia_likes'], df['cuota_votos_real'])\n",
            "rho_late, _ = stats.spearmanr(df['dominancia_late'], df['cuota_votos_real'])\n",
            "\n",
            "print(f\"Spearman Dominancia Total (14 días): rho = {rho_total:.4f}\")\n",
            "print(f\"Spearman Dominancia Tracción Tardía (últimos días): rho = {rho_late:.4f}\")"
        ]
    }
]

notebook_json = {
    "cells": cells,
    "metadata": {
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open('Herramientas/Analisis_Preguntas_Derivadas.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_json, f, indent=2, ensure_ascii=False)

print("Cuaderno Jupyter guardado exitosamente en Herramientas/Analisis_Preguntas_Derivadas.ipynb")
