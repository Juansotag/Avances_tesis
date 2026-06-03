# **Outline de tesis**

**Título:** *Diseño e implementación de un modelo de nowcasting elección-agnóstico para la intención de voto aplicado a elecciones locales en Colombia*

---

## 1. Portada

- Título completo
- Nombre del autor: Juan Sotelo Aguilar
- Institución: Universidad de la Sabana
- Programa: Maestría en Analítica aplicada
- Fecha: 30 de Junio del 2026

---

## 2. Introducción

### 2.1 Motivación del problema
- En Latinoamérica no existen herramientas de seguimiento de la intención de voto más allá de las encuestas.
- Las encuestas en Colombia presentan sesgo y problemas de representatividad (ver críticas de Andrés Caballero, director de Cifras y Conceptos).
- Se hace necesario desarrollar herramientas novedosas para el pronóstico electoral que no dependan de encuestas.

### 2.2 El estado del arte: el modelo SOMEN-DC
- El modelo más relevante es el **SOMEN-DC** (*Social Media Electoral Nowcasting During Campaign*) de Brito & Adeodato (Universidad Federal de Pernambuco, Brasil).
- Usa encuestas e interacciones en redes sociales recopiladas **durante** la campaña electoral para entrenar un modelo específico por elección.
- Problemas identificados:
  1. **Techo encuestocéntrico:** no puede superar la capacidad predictiva de las encuestas porque son su variable objetivo.
  2. **Dependencia de infraestructura costosa:** requiere scraping continuo durante la campaña.
  3. **No transferibilidad:** los modelos solo sirven para la elección en que fueron entrenados.

### 2.3 La hipótesis de trabajo
- Basado en Tumasjan et al. (2010): el número de interacciones de un candidato en redes sociales es un estimador de su capital electoral.
- Añadido propio: al ser un fenómeno común entre elecciones, se puede entrenar un modelo con varias elecciones y usarlo para modelar la intención de voto sin encuestas.
- **Input:** interacciones totales o por publicación en una ventana de tiempo.
- **Output:** vector de tamaño *C* con el % de intención de voto de cada candidato.

### 2.4 Estructura del documento
- Breve descripción de las tres etapas del proyecto: Bolivia (prueba de concepto), Costa Rica (modelado del crecimiento de interacciones) y Colombia (construcción del dataset y modelo final).

---

## 3. Pregunta de investigación

### 3.1 Pregunta principal
- ¿Es posible diseñar un modelo de *nowcasting* de la intención de voto que sea **elección-agnóstico**, no dependa de encuestas? y ¿Puede aplicarse a elecciones locales en Colombia usando únicamente interacciones en redes sociales?

### 3.2 Preguntas derivadas
- ¿Las interacciones en redes sociales de candidatos tienen poder predictivo sobre el resultado electoral?
- ¿Es posible reconstruir el historial de interacciones de publicaciones antiguas sin haber hecho scraping en tiempo real?
- ¿Qué métricas digitales (volumen absoluto, dominancia relativa, crecimiento tardío) son más informativas del resultado electoral?
- ¿Con cuántos datos es viable un modelo de clasificación vs. regresión del voto?

---

## 4. Marco conceptual

### 4.1 Nowcasting electoral y predicción con redes sociales
- Definición de *nowcasting* aplicado a elecciones (estimación en tiempo real de la intención de voto).
- Revisión de la literatura: Tumasjan et al. (2010), Lewis-Beck & Tien (2014), Skoric et al. (2020), Brito & Adeodato (2022, 2023).
- Diferencias entre predicción ex-ante y nowcasting en campañas activas.

### 4.2 Modelos elección-agnósticos: definición y ventajas
- Un modelo elección-agnóstico entrena con datos de múltiples elecciones simultáneamente; sus pesos son transferibles a elecciones no vistas.
- Ventaja respecto al SOMEN-DC: no requiere datos en tiempo real ni encuestas.
- Desarrollo matemático del modelo: explicar como defino matemáticamente el problema, como, a partir de él, construyo como debe lucir las interacciones

### 4.3 Interacciones digitales como proxy de intención de voto
- La hipótesis Tumasjan: volumen de menciones/interacciones ≈ capital electoral.
- Diferencia entre interacciones absolutas y **dominancia relativa** (% de interacciones del candidato sobre el total de la ciudad): la dominancia es más informativa que el volumen absoluto (Spearman ρ > 0.46, p < 2×10⁻⁷ en Colombia).
- Limitaciones: bots, cuentas virales, sesgos de plataforma.

### 4.4 El problema del histórico de interacciones
- Las plataformas no guardan el crecimiento diario de interacciones de publicaciones antiguas.
- Solo el total acumulado hoy es observable, no el que tenía la publicación en el día de la elección.
- Necesidad de un modelo de crecimiento para reconstruir ese histórico.

---

## 5. Objetivo general

Diseñar e implementar un modelo de *nowcasting* de la intención de voto en elecciones locales colombianas que sea elección-agnóstico, no dependa de encuestas, use únicamente interacciones en redes sociales y pueda replicarse con herramientas comerciales accesibles.

### 5.1 Objetivos específicos
1. Replicar y evaluar el modelo SOMEN-DC en un caso real (Bolivia 2025) para confirmar sus limitaciones metodológicas.
2. Modelar el crecimiento temporal de interacciones en redes sociales para habilitar la reconstrucción histórica (Costa Rica 2026).
3. Construir un dataset de entrenamiento elección-agnóstico con elecciones locales colombianas (2023).
4. Entrenar y evaluar modelos de predicción y clasificación del resultado electoral.
5. Validar la viabilidad de la metodología completa y documentar sus limitaciones.

---

## 6. Metodología

### 6.1 Diseño general del pipeline
- Pipeline en tres etapas: (1) Bolivia — prueba de concepto, (2) Costa Rica — calibración del modelo de crecimiento, (3) Colombia — dataset de entrenamiento y modelado final.
- Arquitectura general:
  ```
  Datos actuales de redes sociales (últimos 14 días pre-elección)
      → Modelo Weibull por plataforma (calibrado en Costa Rica)
      → Reconstrucción histórica día a día
      → Features diarias por candidato
      → Modelo elección-agnóstico
      → Vector de intención de voto [c₁, c₂, ..., cₙ]
  ```
- Herramientas usadas: Apify, Twitter API, Playwright, Make.com (sin infraestructura institucional).

### 6.2 Etapa 1 — Bolivia: Replicación del SOMEN-DC y prueba de concepto

#### 6.2.1 Caso de estudio
- Segunda vuelta presidencial de Bolivia (19 de octubre de 2025): Rodrigo Paz Pereira (PDC) vs. Jorge "Tuto" Quiroga (Alianza Libre).
- Resultado real: Paz = 54.53%, Quiroga = 45.47%.

#### 6.2.2 Datos recolectados
- **Ventana temporal:** 180 días previos (18 de mayo al 18 de octubre de 2025).
- **Fuentes:** Facebook, Twitter/X, Instagram y TikTok.
- **Variables:** 29 features por candidato/día: volumen de publicaciones, likes, comentarios, compartidos, retuits, favoritos, métricas por publicación (engagement per post), estandarizadas por red social (z-score).
- **Variable objetivo:** intención de voto interpolada linealmente de encuestas (Ipsos Ciesmori, SPIE, Captura Consulting, Ciemcorp) + resultado electoral como último punto.
- **Dataset final:** 308 registros (154 por candidato), 26 columnas.

#### 6.2.3 Modelos evaluados y resultados
- Regresión Lineal, Regresión Lineal + PCA, MLP-BP, MLP-BP + PCA, GRNN, GRNN + PCA.
- **Mejor modelo:** MLP-BP + PCA → MAE = 0.0279, MAPE ≈ 5.1%, mejor que el baseline (última encuesta, MAE Paz = 0.1803).
- Los modelos lineales fallan (MAE ~0.29–0.31); la relación interacciones–voto no es lineal.

#### 6.2.4 Confirmación de los problemas del SOMEN-DC
- El modelo depende de encuestas como variable objetivo (techo predictivo).
- El scraping continuo durante la campaña no es reproducible sin infraestructura costosa.
- La serie temporal (1 elección, 180 días) no permite generalizar ni entrenar un modelo elección-agnóstico.

### 6.3 Etapa 2 — Costa Rica: Modelado del crecimiento de interacciones

#### 6.3.1 El problema estructural a resolver
- Las plataformas solo muestran el total acumulado actual de interacciones, no el que tenía la publicación en fechas pasadas.
- Para construir el dataset histórico de Colombia 2023 con datos descargados hoy, se necesita estimar cuántas interacciones tenía cada publicación el día de la elección.
- Dos preguntas a resolver: (a) ¿cómo crece el número de interacciones en el tiempo? y (b) ¿los ganadores reciben más interacciones post-victoria?

#### 6.3.2 Metodología de recolección
- Seguimiento diario de publicaciones de candidatos a la presidencia de Costa Rica 2026.
- **Dataset:** 2,026 publicaciones únicas, 19,439 observaciones (pares publicación × día de scraping), 1,922 publicaciones con suficientes datos para el análisis.

#### 6.3.3 Modelo de crecimiento: Weibull con offset
- Curva de crecimiento acumulado modelada con distribución Weibull con offset (*t₀*):
  $$F(t) = 1 - e^{-k \cdot (t + t_0)^\alpha}$$
- **Parámetros calibrados por plataforma:**

| Plataforma | k | α | t₀ (días) | R² panel |
|---|---|---|---|---|
| Facebook | 0.9480 | 0.8230 | 1.93 | 0.3514 |
| Instagram | 1.1369 | 0.5210 | 0.04 | 0.4026 |
| TikTok | 1.3272 | 0.5124 | 0.79 | 0.3509 |
| Twitter/X | 1.4453 | 1.1422 | 0.26 | 0.6905 |

- El R² bajo se debe a que el 66.8% de la varianza es intra-publicación (ruido de medición); la métrica correcta de evaluación es el **MAPE en la estimación del total final**.

#### 6.3.4 Precisión del modelo de crecimiento
- Al día 3 de observación, más del 89–99% de las publicaciones tienen un error < 20% en la estimación del total final.
- El crecimiento es estadísticamente significativo al menos durante 10 días (prueba T, p < 0.0001 para días 1–10), pero económicamente marginal a partir del día 5–7 (< 2% por día). Esto valida una ventana de 14 días pre-elección.

#### 6.3.5 Efecto de la victoria y herramienta de reconstrucción
- La candidata ganadora (Laura Fernández) mostró una curva de saturación más lenta (arrastre post-victoria), pero el efecto no es estadísticamente significativo con un solo caso.
- La calibración Weibull permite estimar la **curva completa de crecimiento día a día** de cualquier publicación histórica, dada su fecha de publicación, las interacciones actuales y (opcionalmente) la fecha de observación.

### 6.4 Etapa 3 — Colombia: Construcción del dataset y modelado

#### 6.4.1 Diseño del dataset de entrenamiento
- Se descargaron interacciones actuales de publicaciones de los últimos **14 días anteriores** a las elecciones de alcaldes (2023) en las **33 ciudades más pobladas de Colombia** (≈ √1,101 municipios).
- **Fuentes:** TikTok, Twitter/X y Facebook (Instagram no disponible por restricciones de Meta).

#### 6.4.2 Criterios de inclusión/exclusión
- Candidatos con **> 10,000 votos** incluidos.
- **Bogotá excluida:** Gustavo Bolívar es influencer masivo; su audiencia no refleja intención de voto local.
- **Piedecuesta excluida:** el candidato ganador eliminó sus cuentas de redes sociales por proceso judicial.
- **Santa Marta:** la candidatura con más votos fue revocada; el segundo candidato es el ganador oficial, pero en el dataset se marca como ganador al candidato con más votos.

#### 6.4.3 Pipeline de scraping (`scrapping_general.py`, `unificar_redes.py`)
- Pipeline automatizado que lee cuentas desde el Excel de resultados electorales y descarga de las tres plataformas.
- **Twitter/X:** Playwright (headless), máx. 50 tweets por candidato.
- **TikTok:** Apify API, máx. 50 videos por candidato.
- **Facebook:** Apify API, máx. 50 posts por candidato.
- Resultado: **5,776 publicaciones** (Facebook 2,511 | Twitter 2,346 | TikTok 919), **123 candidatos únicos**.

#### 6.4.4 Análisis exploratorio (`analisis_exploratorio.ipynb`)
- Universo final: **328 candidatos** en **31 ciudades** (excluidas Bogotá y Piedecuesta).
- **112 candidatos** tienen ≥ 10,000 votos; de estos, el 92.6% tienen publicaciones activas.
- Diferencia de interacciones ganadores vs. no ganadores:
  - Interacciones totales medias: ganadores = 44,252 vs. no ganadores = 28,011.
  - Prueba Mann-Whitney (interacciones por post): p = 0.0481 (significativo al 95%).
  - Tasa de acierto simple: en el **57.58%** de los municipios el candidato con más interacciones ganó.

#### 6.4.5 Reconstrucción del panel histórico (`Reconstruccion_Panel_Historico.ipynb`)
- Se aplica la curva Weibull calibrada en Costa Rica para estimar interacciones día a día.
- El *t₀ individual* de cada post combina el parámetro estructural de la plataforma más la fracción del día transcurrida desde la publicación.
- Dataset resultante: **5,776 publicaciones × 340 columnas** (11 tipos de interacción × 30 días acumulados/nuevos por tipo).
- Validación: monotonicidad perfecta (5,776/5,776) y error mediano en día 14 = 0.000%.

### 6.5 Modelado predictivo

#### 6.5.1 Modelo de regresión (`Modelo_Predictivo_Electoral.ipynb`)
- **Tarea:** predecir el % de votación de cada candidato en su ciudad.
- **Dataset:** 112 candidatos × 84 features; validación: Leave-One-Out CV (LOO-CV).
- **Features principales:** total acumulado al día 14 y crecimiento tardío (d14–d3) por plataforma × 11 tipos de interacción (66 features); totales cross-platform (11); estadísticos globales (7).
- **Mejor modelo:** SVR (RBF) top-5 features → MAE = 15.22 pp, R² = 0.054.
- **Conclusión:** con 112 muestras y 84 features hay sobreajuste estructural. No es viable el modelo de regresión con los datos actuales.

#### 6.5.2 Modelo de clasificación binaria (`Clasificacion_Binaria_Electoral.ipynb`)
- **Reformulación:** ¿quién gana? Clasificación binaria con **dominancia relativa** como feature central (% de interacciones del candidato sobre el total de candidatos trazados en su ciudad).
- **Dataset:** 112 candidatos | 31 ciudades | 27 ganadores (24.1%) | 85 no ganadores (75.9%) | 64 features.
- **Top features:** dominancia_likes (ρ = 0.469), dominancia_engagement (ρ = 0.462), dominancia_comentarios (ρ = 0.426).
- **Mejor modelo:** Regresión Logística (LOO-CV) → Accuracy = 0.812, F1 = 0.488, AUC-ROC = 0.770, acierto a nivel ciudad = 59.3% (16/27).
- **Baseline:** el candidato con mayor dominancia_engagement ganó en el 70.4% de las ciudades (19/27) — supera a todos los modelos entrenados.
- **Conclusión:** la señal predictiva existe (dominancia relativa es significativa), pero con 112 muestras los modelos no superan al baseline; se necesitan más elecciones.

---

## 7. Resultados

### 7.1 Resultados de Bolivia (Etapa 1)
- Confirmación de los problemas del SOMEN-DC.
- MLP + PCA: MAE = 0.0279 (vs. baseline MAE Paz = 0.1803), MAPE ≈ 5.1%.
- La relación interacciones–voto es no lineal; los modelos lineales fallan.
- El giro electoral en la última semana no fue capturado por métricas agregadas simples.
- TikTok mostró dinámicas distintas al resto de plataformas.

### 7.2 Resultados de Costa Rica (Etapa 2)
- Parámetros Weibull calibrados para 4 plataformas con datos de 1,922 publicaciones.
- Al día 3, más del 89–99% de las publicaciones tienen error < 20% en la estimación del total final.
- El crecimiento es estadísticamente significativo durante al menos 10 días, lo que valida la ventana de 14 días.
- Herramienta de reconstrucción histórica disponible y validada (monotonicidad perfecta, error mediano en día 14 = 0%).

### 7.3 Resultados de Colombia (Etapa 3)
- **Señal predictiva confirmada:** las interacciones correlacionan con el resultado (Mann-Whitney p < 0.06; dominancia ρ > 0.46).
- **Dominancia relativa > volumen absoluto:** la posición relativa del candidato en su ciudad es más informativa que el volumen de interacciones.
- **Regresión no viable** con 112 muestras (R² máx = 0.118).
- **Clasificación binaria parcialmente funcional:** acierto de ciudad 59.3% (modelos) vs. 70.4% (baseline).
- **Con más datos, los modelos deberían superar al baseline** al aprender patrones más sutiles.

### 7.4 Síntesis: contribuciones al estado del arte
1. **Elección-agnosticismo:** entrenamiento con múltiples elecciones simultáneamente (a diferencia del SOMEN-DC).
2. **Independencia de encuestas:** variable objetivo = resultados electorales reales.
3. **Reconstrucción histórica Weibull:** permite construir datasets de series temporales para elecciones históricas sin haber hecho scraping en tiempo real.
4. **Viabilidad con herramientas comerciales:** pipeline completo con Apify, Twitter API y Make.com, sin infraestructura institucional.

---

## 8. Impacto esperado

### 8.1 Impacto académico
- Primera metodología de nowcasting electoral elección-agnóstica e independiente de encuestas documentada para Colombia.
- Herramienta de reconstrucción histórica Weibull exportable a otros países y elecciones.
- Contribución metodológica a la literatura de predicción electoral con redes sociales (discusión de viabilidad con distintos tamaños de muestra).

### 8.2 Impacto práctico
- Herramienta de bajo costo reproducible con herramientas comerciales (sin infraestructura universitaria).
- Potencial para medios de comunicación, organizaciones electorales y académicos para monitorear campañas en tiempo real.
- Aplicabilidad a otros países de Latinoamérica donde las encuestas son escasas o poco confiables.

### 8.3 Limitaciones y trabajo futuro
- Calibración Weibull basada en un único caso (Costa Rica 2026); requiere validación con más elecciones.
- Ausencia de Instagram en Colombia reduce cobertura de señales digitales.
- Los modelos son sensibles a candidatos con audiencias atípicas (influencers, candidatos virales).
- No se modela la calidad de la interacción (bots, cuentas falsas, manipulación).
- **Trabajo futuro:** extensión a elecciones legislativas y otros países; ventanas móviles combinadas; integración de señales offline (prensa, economía, territorio); detección de manipulación y bots; validación del modelo Colombia con elecciones futuras.

---

## 9. Conclusión

### 9.1 Respuesta a la pregunta de investigación
- Se demostró que las interacciones en redes sociales **tienen poder predictivo** sobre el resultado electoral en Colombia (p < 0.06, dominancia ρ > 0.46), pero la señal es insuficiente de forma aislada con los datos actuales.
- La metodología de reconstrucción histórica Weibull **es viable y precisa** (error < 20% en el 89–99% de publicaciones al día 3 de observación).
- Un modelo elección-agnóstico **es metodológicamente posible**, pero requiere datos de más elecciones para superar al baseline de dominancia relativa.

### 9.2 Lecciones aprendidas
- La dominancia relativa (posición del candidato en su ciudad) supera al volumen absoluto como predictor.
- La clasificación binaria (¿quién gana?) es más viable que la regresión (¿qué % obtiene?) con muestras pequeñas.
- El giro electoral tardío (última semana) es el fenómeno más difícil de capturar con métricas agregadas.
- El pipeline con herramientas comerciales (Apify, Twitter API, Make.com) es completamente replicable sin infraestructura institucional.

### 9.3 Próximos pasos
- Ampliar el dataset con elecciones de más países y años.
- Recalibrar el modelo Weibull con múltiples casos.
- Validar el modelo Colombia con las elecciones de 2027.

---

## 10. Referencias

- Brito & Adeodato (2022, 2023) — SOMEN-DC (*Social Media Electoral Nowcasting with Dynamic Crawling*)
- Tumasjan et al. (2010) — Twitter como predictor de resultados electorales
- Lewis-Beck & Tien (2014) — Modelos fundamentales de predicción electoral
- Skoric et al. (2020) — Revisión sistemática de redes sociales y elecciones
- Andrés Caballero (Cifras y Conceptos) — Crítica a las encuestas electorales en Colombia
- Ipsos Ciesmori, SPIE, Captura Consulting, Ciemcorp — Encuestas bolivianas 2025 (usadas como benchmark)