# Resumen del proceso de investigación — Nowcasting Electoral con ML y Redes Sociales

**Título tentativo de la tesis:** *Diseño e implementación de un modelo de nowcasting elección-agnóstico para la intención de voto aplicado a elecciones locales en Colombia*

**Autor:** Juan Sotelo Aguilar  

---

## 1. Justificación

En Latinoamérica no existen herramientas de seguimiento de la intención de voto durante elecciones más allá de las encuestas. Estas, tanto por coyuntura interna en Colombia como por intervención y sesgo de los encuestadores, no son una representación fidedigna o insesgada de la intención de voto (ver lo escrito por Andrés Caballero, director de Cifras y Conceptos). Por lo tanto, se hace necesario desarrollar herramientas novedosas para el pronóstico de la intención de voto.

Este proyecto busca desarrollar y probar una metodología para la **estimación de la intención de voto** que:

- **No utilice encuestas** para su funcionamiento.
- Sea **elección-agnóstica**: los pesos y parámetros del modelo sean aplicables a más de una elección y se entrenen con varias elecciones simultáneamente.
- **No necesite levantar datos durante las elecciones**, pudiendo usar datos de elecciones anteriores.

---

## 2. Contexto y estado del arte

### El modelo SOMEN-DC como punto de partida

Existen metodologías que usan ciencia de datos y fuentes abiertas (redes sociales) para pronósticos electorales. El modelo de *nowcasting* más relevante es el **SOMEN-DC** (*Social Media Electoral Nowcasting with Dynamic Crawling*), desarrollado por Brito & Adeodato de la Universidad Federal de Pernambuco (Brasil). Este modelo usa encuestas e interacciones en redes sociales recopiladas **durante** la campaña electoral.

### Problemas identificados en SOMEN-DC

El modelo SOMEN-DC calcula variables del número de interacciones totales de las publicaciones a tiempos regulares, y con esto entrena un modelo específico para cada elección, usando las encuestas como variable objetivo. Esto presenta varios problemas metodológicos:

1. **Techo predictivo encuestocéntrico:** los modelos no tienen forma de superar la capacidad predictiva de las encuestas, ya que estas son su variable objetivo.
2. **Dependencia de infraestructura institucional:** el modelo necesita recopilar datos *durante* la campaña mediante web scraping continuo. Brito & Adeodato accedían a servicios institucionales de la Universidad Federal de Pernambuco que hoy son demasiado costosos o no existen.
3. **No transferibilidad entre elecciones:** los modelos solo son entrenados para una elección específica, sin aprender de otras campañas.

### Hipótesis de trabajo

A partir del trabajo de Tumasjan, partimos de la hipótesis de que **el número de interacciones de un candidato en redes sociales es un estimador de su capital electoral** y, por extensión, de su intención de voto. Añadimos que, al ser un fenómeno común entre elecciones, esto debería permitir entrenar un modelo con varias elecciones y usarlo para modelar día a día la intención de voto sin depender de las encuestas.

El modelo propuesto tendría:
- **Input:** interacciones totales o por publicación en una ventana de tiempo.
- **Output:** vector de tamaño *C* (número de candidatos), donde cada elemento representa el % de intención de voto del candidato *cᵢ*, con *i* ∈ {1, ..., C}.

---

## 3. Etapa 1 — Bolivia: Replicación del SOMEN-DC y prueba de concepto

### Objetivo

Verificar si el modelo SOMEN-DC tiene los problemas metodológicos identificados y si es replicable. El caso de estudio fue la **segunda vuelta presidencial de Bolivia (19 de octubre de 2025)** entre **Rodrigo Paz Pereira (PDC)** y **Jorge "Tuto" Quiroga (Alianza Libre)**.

### Datos recolectados

- **Ventana temporal:** 180 días previos a la elección (18 de mayo al 18 de octubre de 2025).
- **Fuentes:** Facebook, Twitter/X, Instagram y TikTok.
- **Herramientas:** Apify, Twitter API, orquestadas con Make.com.
- **Variables:** 29 features por candidato y día, incluyendo volumen de publicaciones, likes, comentarios, compartidos, retuits, favoritos y métricas normalizadas por publicación (engagement per post). Estandarizadas por red social (z-score).
- **Variable objetivo:** intención de voto interpolada linealmente a partir de encuestas de Ipsos Ciesmori, SPIE, Captura Consulting y Ciemcorp, más el resultado electoral oficial como último punto.
- **Dataset final:** 308 registros (154 por candidato × 2 candidatos), 26 columnas.

### Modelos evaluados

| Modelo | Predicción Paz | Predicción Quiroga | MAE Paz | MAE Quiroga |
|---|---|---|---|---|
| **Baseline (última encuesta)** | 0.3650 | 0.4490 | 0.1803 | 0.0057 |
| Regresión Lineal | 0.2485 | 0.7515 | 0.2968 | 0.2968 |
| Regresión Lineal + PCA | 0.2338 | 0.7662 | 0.3115 | 0.3115 |
| MLP-BP | 0.4691 | 0.5309 | 0.0762 | 0.0762 |
| **MLP-BP + PCA** | **0.5174** | **0.4826** | **0.0279** | **0.0279** |
| GRNN | 0.3467 | 0.6533 | 0.1986 | 0.1986 |
| GRNN + PCA | 0.3448 | 0.6552 | 0.2005 | 0.2005 |

> **Resultado real de la elección:** Paz = 54.53%, Quiroga = 45.47%

**Mejores hiperparámetros encontrados:**
- **MLP:** `hidden_layer_sizes=(48, 24)`, `learning_rate_init=0.001`, `alpha=0.01` → MAE_CV = 0.1818
- **GRNN:** `sigma=0.8`, `k=0.5` → MAE_CV = 0.1285

### Hallazgos principales — Bolivia

1. **Los modelos lineales fallan** en capturar la relación entre actividad digital e intención de voto (MAE ~0.29–0.31, hasta 10 veces peor que MLP+PCA).
2. **MLP con PCA es el mejor modelo:** MAE = 0.0279, MAPE ≈ 5.1% (Paz), un error 6–10 veces menor que los modelos lineales y menor que el baseline encuesta (MAE Paz = 0.1803).
3. **GRNN muestra desempeño intermedio** pero no supera al MLP+PCA.
4. Las métricas digitales **no reflejan linealmente** el resultado electoral, pero **contienen señal predictiva relevante cuando se modelan de forma no lineal**.
5. El giro electoral ocurrió en la última semana y no fue capturado por métricas agregadas simples.
6. TikTok mostró dinámicas distintas al resto de redes.
7. La combinación **PCA + MLP logra capturar factores latentes comunes entre plataformas**.

### Limitaciones del estudio boliviano

- Serie temporal muy corta (180 días, un solo balotaje).
- Cambios abruptos de *momentum* electoral en la última semana.
- Posibles sesgos de audiencia por plataforma.
- Imposibilidad de generalizar con un único caso de estudio.

---

## 4. Etapa 2 — Costa Rica: Modelado del crecimiento de interacciones

### Problema que motivó este estudio

Tras confirmar los problemas del SOMEN-DC en Bolivia, surgió una limitación estructural: **ninguna red social guarda el histórico del crecimiento de interacciones día a día de publicaciones antiguas**. Las interacciones que vemos hoy en una publicación de hace dos años incluyen todas las reacciones acumuladas hasta hoy, no las que tenía el día de la elección. Esto imposibilita construir un dataset histórico de elecciones pasadas.

Para resolver esto, se necesitaba responder dos preguntas:

1. ¿**Cómo crece el número de interacciones** de una publicación en el tiempo, y cuándo se detiene ese crecimiento?
2. ¿Las publicaciones de candidatos **ganadores** reciben más interacciones **después de ganar** que las de los perdedores?

### Metodología

Se levantaron **diariamente** las interacciones de las publicaciones de los candidatos a la presidencia de Costa Rica 2026 durante el período electoral. El dataset final incluyó:

- **2,026 publicaciones únicas** seguidas en el tiempo.
- **19,439 observaciones** (pares publicación × día de scraping).
- **1,922 publicaciones** con suficientes observaciones para el panel analítico (mínimo 2 observaciones y máximo en día ≥ 3).
- **14,596 pares** (día relativo, fracción) en el panel de fracciones.

Se modeló la curva de crecimiento acumulado de interacciones con una **distribución Weibull con offset** (*t0*):

$$F(t) = 1 - e^{-k \cdot (t + t_0)^\alpha}$$

### Parámetros calibrados por plataforma (Costa Rica 2026)

| Plataforma | k | α | t₀ (días) | t₀ (horas) | R² panel | n publicaciones |
|---|---|---|---|---|---|---|
| **Facebook** | 0.9480 | 0.8230 | 1.9323 | 46.4 h | 0.3514 | 765 |
| **Instagram** | 1.1369 | 0.5210 | 0.0408 | 1.0 h | 0.4026 | 603 |
| **TikTok** | 1.3272 | 0.5124 | 0.7887 | 18.9 h | 0.3509 | 344 |
| **Twitter/X** | 1.4453 | 1.1422 | 0.2566 | 6.2 h | 0.6905 | 210 |

> **Nota sobre R² bajo:** La descomposición de varianza reveló que el 66.8% de la varianza es varianza *dentro* de las publicaciones (ruido de medición) y solo el 29.2% es varianza *entre* publicaciones. El R² bajo sobre el panel es irreducible dado este nivel de heterogeneidad, y **no es la métrica adecuada para evaluar el modelo**. La métrica correcta es el error en la estimación del total final.

### Error en estimación del total final (MAPE mediano por día de observación)

| Plataforma | Día 0 | Día 1 | Día 2 | Día 3 | Día 7 |
|---|---|---|---|---|---|
| **Facebook** | 11.3% | 6.9% | 3.7% | 2.1% | 0.3% |
| **Instagram** | 64.8% | 20.7% | 15.7% | 12.1% | 3.8% |
| **TikTok** | 25.4% | 14.2% | 8.3% | 5.9% | 2.3% |
| **Twitter/X** | 56.4% | 11.1% | 2.5% | 0.4% | 0.0% |

**Publicaciones con error < 20% observando en el Día 3:**
- Facebook: **99.0%** (472/477)
- Instagram: **89.7%** (530/591)
- TikTok: **93.3%** (321/344)
- Twitter/X: **99.5%** (204/205)

### Significancia estadística del crecimiento (prueba T de una muestra vs. 0)

| Día relativo | Crecimiento promedio de likes (%) | Estado | p-valor |
|---|---|---|---|
| Día 1 | 2.87% | ACTIVO | < 0.0001 |
| Día 2 | 5.15% | ACTIVO | < 0.0001 |
| Día 3 | 8.91% | ACTIVO | < 0.0001 |
| Día 4 | 3.23% | ACTIVO | < 0.0001 |
| Día 5 | 1.85% | ACTIVO | < 0.0001 |
| Día 6 | 1.39% | ACTIVO | < 0.0001 |
| Día 7 | 1.12% | ACTIVO | < 0.0001 |
| Día 8 | 0.87% | ACTIVO | < 0.0001 |
| Día 9 | 0.62% | ACTIVO | < 0.0001 |
| Día 10 | 0.46% | ACTIVO | < 0.0001 |

> **Conclusión:** El crecimiento es estadísticamente significativo durante al menos 10 días, pero económicamente marginal a partir del día 5–7 (menos del 2% de crecimiento por día). Esto valida la ventana de 7 a 12 días mencionada en la literatura y orienta el uso de los últimos 14 días pre-elección en Colombia.

### Efecto de victoria (Costa Rica)

La candidata ganadora (**Laura Fernández**) mostró una curva de saturación más lenta que el resto de candidatos, lo que indica que el triunfo genera un "arrastre" de interacciones en publicaciones antiguas. Sin embargo, este efecto **no es estadísticamente significativo** con los datos disponibles de este único caso.

### Herramienta derivada: reconstrucción histórica

La calibración de la curva Weibull por plataforma permite, dados:
- La fecha de publicación de un post.
- El número de interacciones actuales observadas.
- (Opcional) La fecha en que se realizó la observación.

...estimar la **curva completa de crecimiento día a día** que tuvo ese post desde su publicación. Esto es la clave metodológica que hace viable el entrenamiento del modelo con elecciones históricas.

**Ejemplo de reconstrucción (Facebook, total final 50.000 likes):**

| Día relativo | % Acumulado | Interacciones estimadas | Interacciones nuevas ese día |
|---|---|---|---|
| 0 | 80.4% | 40,206 | 40,206 |
| 1 | 89.9% | 44,977 | 4,771 |
| 2 | 94.6% | 47,319 | 2,342 |
| 3 | 97.1% | 48,528 | 1,209 |
| 5 | 99.1% | 49,529 | 354 |
| 7 | 99.7% | 49,841 | 113 |
| 10 | 99.9% | 49,966 | 22 |

---

## 5. Etapa 3 — Colombia: Construcción del dataset de entrenamiento y modelamiento

### Diseño del dataset

Con la herramienta de reconstrucción histórica Weibull calibrada en Costa Rica, se procedió a construir el dataset de entrenamiento para el modelo elección-agnóstico. Se descargaron las interacciones **actuales** de las publicaciones de los últimos **14 días anteriores** a las elecciones de alcaldes en las **33 ciudades más pobladas de Colombia** (número derivado de √1,101 municipios).

**Fuentes de datos:** TikTok, Twitter/X y Facebook. Por restricciones propias de Meta, **no fue posible levantar información de Instagram**.

### Criterios de inclusión y exclusión de candidatos y ciudades

- Se incluyeron todos los candidatos con **más de 10.000 votos** (umbral derivado de los datos; candidatos con menos votos en su mayoría eran candidatos sin posibilidades reales).
- **Bogotá:** excluida por la presencia de Gustavo Bolívar, influencer masivo cuya audiencia en redes no refleja intención de voto local y causaba errores en el entrenamiento.
- **Piedecuesta (Santander):** excluida porque el candidato ganador eliminó sus cuentas de redes sociales por estar en un proceso judicial.
- **Santa Marta:** la candidatura con más votos fue revocada; el segundo candidato quedó como ganador. Dentro del dataset, el candidato con más votos es marcado como ganador, independientemente de lo que ocurrió después.

### Resultados electorales disponibles

La carpeta `Colombia/Formatos e26/` contiene los formularios E-26 (resultados electorales oficiales) de todas las 33 ciudades incluidas:

Apartadó, Armenia, Barrancabermeja, Barranquilla, Bello, Bogotá (excluida), Bucaramanga, Buenaventura, Cali, Cartagena, Cúcuta, Dosquebradas, Envigado, Floridablanca, Ibagué, Itagüí, Manizales, Medellín, Montería, Neiva, Palmira, Pasto, Pereira, Piedecuesta (excluida), Popayán, Riohacha, Sincelejo, Soacha, Soledad, Tunja, Valledupar, Villavicencio.

---

## 5a. Recolección de datos — Colombia (`scrapers/`, `scrapping_general.py`, `unificar_redes.py`)

### Pipeline de scraping

Se construyó un pipeline de scraping automatizado (`scrapping_general.py`) que lee las cuentas de los candidatos desde el Excel de resultados electorales y las descarga de las tres plataformas de manera modular:

| Plataforma | Herramienta | Parámetros |
|---|---|---|
| **Twitter/X** | Playwright (navegador headless) | Máx. 50 tweets por candidato |
| **TikTok** | Apify API | Máx. 50 videos por candidato |
| **Facebook** | Apify API | Máx. 50 posts por candidato |

Los scrapers operan candidato por candidato, registrando el estado de cada extracción en `resultados/reporte_proceso.csv`. Los datos crudos se guardan en archivos separados: `tweets_full.csv`, `tiktok_full.csv`, `facebook_full.csv`.

### Unificación del dataset crudo (`unificar_redes.py`)

El script homogeniza los esquemas de las tres plataformas en un **esquema común** (`resultados/redes_unificadas.csv`) con columnas compartidas: `id_candidato | red_social | fecha | hora | usuario | texto | url | likes | comentarios | compartidos | vistas | favoritos`. Para Facebook se preservan adicionalmente las reacciones detalladas: `fb_love`, `fb_haha`, `fb_care`, `fb_wow`, `fb_sad`, `fb_angry`.

**Resultado del scraping unificado:**
- **5,776 publicaciones** cargadas (95 filas sin fecha/hora excluidas).
- **Distribución:** Facebook 2,511 | Twitter 2,346 | TikTok 919.
- **Candidatos únicos:** 123 | **Rango de fechas:** 2023-10-21 → 2023-10-29.

---

## 5b. Análisis Exploratorio — datos crudos (`analisis_exploratorio.ipynb`)

### Universo electoral

Tras excluir Piedecuesta y Bogotá: **328 candidatos** en **31 ciudades**.
- **121 candidatos** tienen ≥ 10,000 votos.
- **112 candidatos** (34.1%) tienen publicaciones activas. De estos, 92.6% son candidatos con ≥ 10k votos.
- Distribución de redes activas: 28 con solo 1 red, 38 con 2 redes, 46 con las 3 redes.

| Red social | Candidatos activos | % del total |
|---|---|---|
| Facebook | 97 | 29.6% |
| TikTok | 76 | 23.2% |
| Twitter/X | 69 | 21.0% |

### Interacciones promedio por publicación, por plataforma

| Plataforma | Likes | Comentarios | Compartidos | Vistas |
|---|---|---|---|---|
| **Facebook** | 392.2 | 76.1 | 72.6 | 9,144.6 |
| **TikTok** | 1,246.2 | 59.9 | 54.7 | 26,154.5 |
| **Twitter/X** | 338.5 | 58.0 | 120.1 | 16,946.0 |

### Ganadores vs. no ganadores

| Grupo | Int. totales (media) | Int. promedio/post | Nº posts (media) | Votos (media) |
|---|---|---|---|---|
| **No ganadores** | 28,011.7 | 381.1 | 45.3 | 44,674.4 |
| **Ganadores** | 44,252.9 | 759.9 | 52.5 | 159,241.8 |

- Mediana: Ganadores = 12,598 | No ganadores = 5,662.
- **Prueba Mann-Whitney U** (interacciones totales): U = 1725.5, **p = 0.0515** → significativo al 90%.
- **Prueba Mann-Whitney U** (interacciones promedio/post): **p = 0.0481** → significativo al 95%.
- **Tasa de acierto simple:** en el **57.58%** de los municipios (19/33), el candidato con más interacciones totales ganó.

> La señal existe pero no es suficiente de forma aislada: las interacciones correlacionan con el resultado electoral, pero la relación es débil para predicción directa.

---

## 5c. Reconstrucción del Panel Histórico (`Reconstruccion_Panel_Historico.ipynb`)

### Lógica de reconstrucción

Se aplica la curva Weibull calibrada en Costa Rica para estimar las interacciones día a día. El *t₀ individual* de cada post combina el parámetro estructural de la plataforma (`t₀_base` del `weibull_params.csv`) más la fracción del día transcurrida desde la publicación hasta las 23h:

$$t_0^{\text{post}} = t_0^{\text{base}} + \frac{23 - \text{hora\_pub}}{24}$$

Las interacciones estimadas para cada día relativo `t` son:

$$\text{acum}_{d_t} = \text{total\_final} \times \frac{F(t,\, t_0^{\text{post}})}{F(14,\, t_0^{\text{post}})}$$

### Dataset panel histórico resultante

| Dimensión | Valor |
|---|---|
| Filas (publicaciones) | 5,776 |
| Columnas totales | 340 |
| Tipos de interacción reconstruidos | 11 (likes, comentarios, compartidos, vistas, favoritos + 6 reacciones FB) |
| Columnas por tipo | 30 (15 acumuladas d0–d14 + 15 nuevas d0–d14) |

**t₀ individual por plataforma (media):** Facebook 2.298 | TikTok 1.155 | Twitter/X 0.669.  
**% de likes acumulado en el día 0 (mediana):** Facebook 84.7% | TikTok 75.0% | Twitter/X 30.4%.

### Validación (`EDA_panel_historico.ipynb`)

- **Monotonicidad:** 5,776/5,776 publicaciones sin violaciones. ✓
- **Consistencia:** error mediano en día 14 = **0.000%** para los 11 tipos de interacción; p95 = 0.000%. ✓
- **Diferencias entre plataformas:** Kruskal-Wallis H = 1,109.23, p = 1.36×10⁻²⁴¹ → justifica tratar cada red con escalas distintas.
- **Consistencia interna Facebook:** Spearman likes vs. comentarios = 0.836, p ≈ 0.

---

## 5d. Modelo Predictivo de Regresión (`Modelo_Predictivo_Electoral.ipynb`)

### Objetivo

Predecir el **porcentaje de votación** de cada candidato respecto al total de votos de candidatos trazados en su ciudad. **No es serie de tiempo:** los 14 días de interacciones se aplanan como features tabulares. Dataset: **112 candidatos × 84 features**. Validación: **Leave-One-Out CV (LOO-CV)**.

Las 84 features incluyen: total acumulado al d14 y crecimiento tardío (d14–d3) por plataforma × 11 tipos de interacción = 66 features; totales cross-platform = 11 features; estadísticos globales = 7 features.

### Features más correlacionadas con % votos (Spearman)

| Feature | ρ | p-valor |
|---|---|---|
| twitter_likes_total | 0.403 | 0.000010 |
| twitter_vistas_total | 0.394 | 0.000018 |
| twitter_vistas_late_growth | 0.386 | 0.000026 |
| twitter_comentarios_total | 0.375 | 0.000045 |
| total_fb_care | 0.359 | 0.000103 |
| facebook_fb_love_late_growth | 0.353 | 0.000132 |
| avg_interactions_per_post | 0.311 | 0.000862 |

Twitter domina las correlaciones directas con votos; las reacciones afectivas de Facebook (fb_care, fb_love) son señales latentes relevantes.

### Resultados de regresión (LOO-CV, 84 features)

| Modelo | MAE (pp) | RMSE | R² | MAPE |
|---|---|---|---|---|
| **SVR (RBF)** | **15.46** | 19.79 | 0.028 | 138.1% |
| Random Forest | 15.70 | 19.26 | **0.079** | 158.4% |
| ElasticNet | 16.93 | 22.49 | -0.256 | 162.1% |
| Lasso | 17.25 | 23.17 | -0.332 | 157.2% |
| Gradient Boosting | 17.45 | 21.46 | -0.143 | 165.3% |
| Ridge | 18.58 | 28.86 | -1.068 | 161.5% |
| MLP (PyTorch) | 19.60 | 30.54 | -1.316 | 206.7% |
| MLP (sklearn) | 20.36 | 25.64 | -0.632 | 137.7% |

**Con reducción de dimensionalidad (top-K features / PCA):**

| Configuración | MAE (pp) | RMSE | R² |
|---|---|---|---|
| **SVR (RBF) top-5** | **15.22** | 19.52 | 0.054 |
| SVR (RBF) top-10 | 15.22 | 19.29 | 0.076 |
| Random Forest top-5 | 15.30 | 18.85 | **0.118** |
| SVR (RBF) PCA-15 (98.8% var) | 15.45 | 19.83 | 0.023 |

> **Conclusión:** El mejor modelo es SVR (RBF) top-5 (MAE = 15.22 pp, R² = 0.054). Con 112 muestras y 84 features hay sobreajuste estructural. Los errores más grandes se producen en candidatos con alta dominancia electoral (>80%): Rojas Giraldo en Manizales (real: 84%, predicho: 14%) y Char en Barranquilla (real: 85%, predicho: 34%). Las ciudades con menor error: Cartagena (MAE=6.6), Valledupar (7.6), Pereira (7.7). Mayor error: Manizales (36.0), Barrancabermeja (27.7).

---

## 5e. Transición al modelo de Clasificación Binaria (`Clasificacion_Binaria_Electoral.ipynb`)

### Motivación del cambio de paradigma

El modelo de regresión demostró que con **solo 112 muestras** no es posible predecir el porcentaje de votos con utilidad práctica (R² máximo = 0.118). La pregunta real es más simple: ¿**quién gana**? Se reformula como **clasificación binaria**, introduciendo la **dominancia relativa** como feature central: % de las interacciones del candidato sobre el total de todos los candidatos trazados en su ciudad.

Ventajas del cambio:
1. Clasificación binaria es más factible con pocos datos.
2. La métrica natural es la exactitud a nivel ciudad (en cuántas ciudades se predice bien al ganador).
3. La dominancia relativa captura la posición relativa del candidato, más informativa que el volumen absoluto.

### Dataset de clasificación

- **112 candidatos | 31 ciudades | 27 ganadores (24.1%) | 85 no ganadores (75.9%)**
- **64 features** incluyendo dominancia relativa, posts/día, días activos y métricas de interacción.

### Top features más correlacionadas con ganar (Spearman)

| Feature | ρ Spearman | p-valor |
|---|---|---|
| **dominancia_likes** | **0.469** | 1.82×10⁻⁷ |
| **dominancia_engagement** | **0.462** | 2.94×10⁻⁷ |
| dominancia_comentarios | 0.426 | 2.86×10⁻⁶ |
| dominancia_compartidos | 0.412 | 6.29×10⁻⁶ |
| dominancia_vistas | 0.370 | 6.05×10⁻⁵ |
| n_candidatos_ciudad (negativo) | -0.261 | 5.36×10⁻³ |
| total_likes | 0.257 | 6.30×10⁻³ |

### Resultados de clasificación (LOO-CV, top-15 features)

| Modelo | Accuracy (candidato) | F1 | AUC-ROC | Accuracy (ciudad) |
|---|---|---|---|---|
| **Logistic Regression** | **0.812** | **0.488** | **0.770** | **59.3% (16/27)** |
| Random Forest | 0.741 | 0.326 | 0.709 | 51.9% (14/27) |
| MLP | 0.598 | 0.483 | 0.731 | 51.9% (14/27) |
| SVM (RBF) | 0.714 | 0.238 | 0.502 | 40.7% (11/27) |
| Gradient Boosting | 0.705 | 0.327 | 0.657 | 40.7% (11/27) |

**Reporte del mejor modelo (Logistic Regression):**

| Clase | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| No Gana | 0.83 | 0.95 | 0.89 | 85 |
| Gana | 0.71 | 0.37 | 0.49 | 27 |
| **Accuracy** | | | **0.81** | **112** |

### Baseline vs. mejor modelo

| Enfoque | Acierto a nivel ciudad |
|---|---|
| **Baseline (mayor dominancia_engagement = ganador)** | **70.4% (19/27)** |
| Logistic Regression (LOO-CV) | 59.3% (16/27) |

> **Hallazgo clave:** el baseline simple supera a todos los modelos entrenados. La señal más relevante (dominancia relativa) ya predice correctamente el 70% de las ciudades sin entrenamiento. Esto indica que, con más datos, los modelos podrían aprender patrones más sutiles que superen al baseline.

### Ciudades correctamente predichas — Logistic Regression

✅ **Aciertos (16):** Soacha, Sincelejo, Santa Marta, Riohacha, Pereira, Pasto, Manizales, Neiva, Medellín, Tunja, Floridablanca, Envigado, Buenaventura, Barranquilla, Palmira, Valledupar.

❌ **Errores (11):** Apartadó, Itagüí, Dosquebradas, Montería, Cali, Cartagena, Bello, Soledad, Barrancabermeja, Armenia, Bucaramanga.

### Implicaciones para la tesis

1. Las interacciones en redes **sí tienen poder predictivo** (Mann-Whitney p<0.06, Spearman dominancia ρ>0.46).
2. La **dominancia relativa** (posición en la ciudad) > interacciones absolutas.
3. El modelo de regresión **no es viable** con 112 muestras; la clasificación binaria es más prometedora.
4. Se necesitan **más elecciones y más ciudades** para que los modelos superen al baseline y desarrollar el modelo elección-agnóstico completo.

---

## 6. Arquitectura metodológica general

```
Datos actuales de redes sociales
(publicaciones de los últimos 14 días pre-elección, cosechadas hoy)
              │
              ▼
    Modelo Weibull por plataforma
    (calibrado en Costa Rica 2026)
              │
              ▼
    Reconstrucción histórica día a día
    de las interacciones por candidato
              │
              ▼
    Features diarias: likes, comentarios,
    compartidos, vistas, posts (por plataforma)
              │
              ▼
    Modelo elección-agnóstico
    (entrenado con múltiples elecciones)
              │
              ▼
    Vector de intención de voto [c₁, c₂, ..., cₙ]
    (sin usar encuestas)
```

---

## 7. Contribuciones principales a la literatura

1. **Elección-agnosticismo:** el modelo se entrena con datos de múltiples elecciones, a diferencia de SOMEN-DC que entrena un modelo por elección.
2. **Independencia de encuestas:** la variable objetivo no son las encuestas sino los resultados electorales reales.
3. **Reconstrucción histórica Weibull:** la herramienta permite construir datasets de series temporales de interacciones para elecciones históricas, sin necesidad de haber hecho scraping durante las campañas.
4. **Viabilidad con herramientas comerciales:** el pipeline completo usa únicamente Apify, Twitter API y Make.com, sin infraestructura institucional costosa.

---

## 8. Limitaciones generales

- La calibración Weibull está basada en un único caso (Costa Rica 2026) y requiere validación en más elecciones.
- El efecto de la victoria post-electoral sobre las interacciones no es estadísticamente significativo con un solo caso.
- La ausencia de Instagram en Colombia reduce la cobertura de señales digitales.
- Los modelos son sensibles a candidatos con audiencias atípicas (influencers, candidatos virales).
- No se modela la calidad de la interacción (bots, cuentas falsas, manipulación).

---

## 9. Trabajo futuro

- Extensión a elecciones legislativas y locales de otros países.
- Ventanas móviles combinadas (diarias + mensuales).
- Integración de señales offline (prensa, territorio, economía).
- Detección de manipulación, bots y calidad de interacción.
- Recalibración del modelo Weibull con más casos de estudio.
- Validación del modelo Colombia con elecciones futuras.

---

## 10. Referencias principales

- Brito & Adeodato (2022, 2023) — SOMEN-DC
- Tumasjan et al. (2010) — Twitter como predictor de resultados electorales
- Lewis-Beck & Tien (2014) — modelos fundamentales de predicción electoral
- Skoric et al. (2020) — revisión sistemática de redes sociales y elecciones