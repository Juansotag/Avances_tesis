# Guión de Presentación: ELA-NOM
## Tesis de Maestría · 30 minutos · Versión v2 (post-reunión director)

---

> **Nota de uso:** Los bloques en *[cursiva con corchetes]* son acotaciones del presentador, no se leen en voz alta. Los marcadores **[P1]**, **[PM2]**, etc. señalan el momento en que cada pregunta queda respondida. Los números clave están en **negrita**.

---

## SALUDO FORMAL

*[De pie, antes de avanzar la primera diapositiva]*

Buenas tardes a todos los presentes. A los jurados, el doctor Andrés Cruz, el doctor César Caballero y el profesor Adrián Santana. También a mi director de trabajo de grado, el doctor Miguel Uribe Laverde, y a todos los asistentes.

Me llamo **Juan Sotelo Aguilar** y hoy busco presentar mi trabajo de grado para optar por el título de **Magíster en Analítica Aplicada de la Universidad de La Sabana**, con el trabajo titulado:

**"Diseño e implementación del modelo ELA-NOM: un nowcasting elección-agnóstico para la intención de voto aplicado a elecciones locales en Colombia 2023."**

---

## BLOQUE 1 — El problema: ¿por qué necesitamos alternativas al pronóstico electoral? (2 min)

*[Diapositiva 1: cifras globales / industria]*

La industria global de investigación de mercados y opinión pública facturó **153 mil millones de dólares en 2024**. Es una industria enorme, pero que enfrenta tres presiones simultáneas.

La primera es la presión competitiva global. Plataformas de predicción alternativas como Polymarket y Kalshi ya mueven más de **un billón de dólares** en contratos de predicción electoral. Sus valuaciones y ganancias anualizadas superan los **mil millones de dólares para 2026**. El mercado está votando con su dinero: quiere pronósticos ágiles, baratos y en tiempo real.

La segunda es una presión regulatoria local. En Colombia, la **Ley 2494 de 2025** endureció sustancialmente las condiciones para publicar encuestas electorales, encareciendo los costos hasta el punto de que algunas de las firmas demoscópicas más grandes han cesado operaciones en el país.

La tercera es una presión estructural de cobertura. Tenemos más de **1.100 municipios**. La cobertura encuestadora llega con suerte a 10 o 12 ciudades. Alcaldes y gobernadores son los cargos más cercanos al ciudadano y prácticamente no tienen cobertura demoscópica.

Estos tres factores crean una necesidad clara: **metodologías de pronóstico electoral ágiles, baratas e innovadoras**.

---

## BLOQUE 2 — La ruta que siguió la literatura (2 min)

*[Diapositiva 2: línea de tiempo de la literatura]*

Los modelos de pronóstico electoral están dominados por los modelos de **nowcasting**: en lugar de proyectar una variable al futuro, buscan estimar el valor actual de una variable subyacente difícil de medir — en nuestro caso, la **cuota de voto** de un candidato.

Desde los años 70 en el mundo anglosajón se desarrollaron estos modelos: primero con variables de popularidad, luego añadiendo indicadores macroeconómicos. En 2016 llegó el quiebre: prácticamente ninguno anticipó la victoria de Trump ni el Brexit.

La alternativa llegó desde el machine learning. El trabajo seminal de **Tumasjan** en 2009 para las elecciones del Parlamento Alemán mostró que con **100.000 tweets** era posible pronosticar el porcentaje de voto de cada partido con un error promedio inferior al **2%**. Era la primera demostración seria de que las publicaciones en redes sociales eran un estimador razonablemente insesgado de la cuota electoral.

Los trabajos que siguieron escalaron masivamente — Tsakalidis en 2018 usó más de **catorce millones de tweets** — pero toda la evidencia seguía concentrada en Europa y Norteamérica.

*[Diapositiva 3: los tres problemas del SOMEN-DC]*

El primer trabajo en abordar ambas brechas en América Latina es el de **Kellyton Brito y Paulo Andeoato**, de la Universidad Federal de Pernambuco. Su metodología **SOMEN-DC** propone usar las **interacciones de las publicaciones de los candidatos**, no de los votantes. Con eso logró errores de entre 2 y 7% en elecciones presidenciales de cuatro países latinoamericanos.

Sin embargo, el modelo tiene tres limitaciones estructurales no resueltas. Primera: es un modelo de elección única — los pesos no pueden exportarse a otra elección. Segunda: depende de las encuestas como variable objetivo de entrenamiento, heredando sus errores. Tercera: requiere scraping diario desde el primer día de campaña, lo que cierra la posibilidad de usar elecciones pasadas como entrenamiento.

La tercera limitación es la más grave: un modelo que no puede aprender de elecciones pasadas no es realmente generalizable.

---

## BLOQUE 3 — La pregunta de investigación (1,5 min)

*[Diapositiva 4 y 5: preguntas P y PM]*

Esas limitaciones llevaron a la pregunta central:

> *¿Es posible diseñar un modelo de nowcasting electoral **elección-agnóstico** — cuyos parámetros se entrenen con múltiples contiendas pasadas y sean transferibles — que opere **sin encuestas**, usando exclusivamente señales de redes sociales?*

Cuatro preguntas derivadas estructuran el diseño:

- **P1:** ¿Las interacciones tienen poder predictivo real sobre la cuota de voto en Colombia?
- **P2:** ¿Es posible reconstruir matemáticamente el historial de interacciones de publicaciones pasadas sin haber hecho scraping en tiempo real?
- **P3:** ¿Qué señal digital es la más informativa y robusta?
- **P4:** ¿Cuántas contiendas de entrenamiento son necesarias para desempeño estable?

Y cuatro preguntas metodológicas:

- **PM1:** ¿El SOMEN-DC es replicable con herramientas comerciales sin APIs académicas?
- **PM2:** ¿Cómo se comporta el SOMEN-DC ante un cambio en su lógica de recolección?
- **PM3:** ¿Cómo se construye un dataset de entrenamiento retroactivo para este problema?
- **PM4:** ¿Cómo se convierte el modelo en una herramienta de nowcasting siendo un problema transversal y no de series de tiempo?

---

## BLOQUE 4 — Diseño de tres etapas (0,5 min)

*[Diapositiva 6: diagrama de tres etapas]*

El objetivo general fue diseñar, implementar y validar ese modelo. Lo llamamos **ELA-NOM**: Election-Agnostic Nowcasting Model.

El diseño tuvo tres etapas. Bolivia responde PM1 y PM2. Costa Rica responde P2 y PM3. Colombia responde P1, P3 y P4. Y la validación con las elecciones presidenciales de 2026 responde PM4.

---

## BLOQUE 5 — Etapa 1: Bolivia (4 min)

*[Diapositiva 7: Bolivia — diseño]*

El primer paso fue replicar el SOMEN-DC. La razón es simple: el trabajo de Brito y Andeoato requirió una alianza institucional entre Meta y la Universidad de Pernambuco a la que la Universidad de La Sabana no tiene acceso. Era necesario verificar que era posible obtener resultados comparables con herramientas comerciales abiertas.

Seleccionamos la **segunda vuelta presidencial de Bolivia del 19 de octubre de 2025**: Rodrigo Paz Pereira contra Jorge Quiroga. Elección bipolar, latinoamericana, no tratada por los autores del SOMEN-DC.

El dataset: **153 días de campaña**, extracción diaria en cuatro plataformas durante la última semana de campaña, **308 observaciones, 26 características**. La variable objetivo se construyó interpolando linealmente **14 encuestas**, anclada al resultado real: Paz **54,53%**, Quiroga **45,47%**.

*[Diapositiva 8: serie de tiempo Bolivia]*

*[Diapositiva 9: tabla de resultados]*

Se entrenaron seis especificaciones. El **MLP-BP con PCA** fue el mejor: predijo **51,74%** para Paz — un error de **2,79 pp**, frente a los **18,03 pp** del baseline de última encuesta. Una mejora de más de seis veces.

Esto responde **PM1**: la replicación del SOMEN-DC es posible con herramientas comerciales.

*[Diapositiva 10: limitaciones confirmadas]*

El ejercicio también confirma **PM2**: las tres limitaciones son empíricamente reales. Los pesos del MLP-BP son específicos de Bolivia y no exportables. El modelo aprendió a seguir las encuestas. Y la dinámica de la última semana no fue capturada.

Conclusión: la señal digital existe, pero el paradigma *during-campaign* no escala. Necesitamos un enfoque diferente.

---

## BLOQUE 6 — Etapa 2: Costa Rica (4,5 min)

*[Diapositiva 11: el problema del histórico]*

Si queremos entrenar ELA-NOM con elecciones pasadas, necesitamos saber cuántas interacciones tenían las publicaciones el día anterior a cada elección. El problema: **las plataformas solo muestran el total acumulado hoy**. Una extracción estática de publicaciones de 2023 hecha en 2026 captura tres años de likes, incluyendo el tráfico póstumo generado tras conocerse los resultados.

La solución: modelar la curva de crecimiento de interacciones de una publicación. Si conocemos esa forma, podemos estimar retroactivamente cuántas interacciones existían en cualquier momento pasado usando la fecha de publicación, las interacciones totales y la plataforma.

*[Diapositiva 12: diseño Costa Rica y parámetros]*

La primera vuelta presidencial de Costa Rica del **1 de febrero de 2026** fue el caso de estudio. Durante **30 días** — 15 antes y 15 después — extrajimos diariamente las interacciones de los cuatro candidatos. Resultado: **1.922 publicaciones únicas**, **19.439 pares (día, fracción)**.

La función **Weibull con offset** $F(t) = 1 - e^{-k(t+t_0)^\alpha}$ superó a la exponencial y a la logística en R² promedio: **0,449 versus 0,182 y 0,245**. Sus ventajas: está naturalmente acotada en [0,1], α controla la geometría, y t₀ captura las interacciones previas al primer scraping.

Los parámetros calibrados por plataforma revelan un gradiente coherente: t₀ va de **1 hora para Instagram** hasta **46 horas para Facebook**. Facebook distribuye contenido gradualmente durante casi dos días; Twitter/X y Instagram son plataformas de consumo inmediato. Twitter/X muestra además α > 1, coherente con el mecanismo de retweet acumulativo.

*[Diapositiva 13: la ganadora es indistinguible del resto]*

El hallazgo más importante: la **curva de la candidata ganadora es morfológicamente idéntica a la del resto**. No existe diferencia estadísticamente significativa en el crecimiento entre ganadores y perdedores en ningún día del panel. El patrón es una propiedad de la plataforma, no del candidato. Esto valida la transferibilidad del restaurador.

Esto responde **P2** y **PM3**.

*[Diapositiva 14: MAPE y convergencia]*

A partir del **Día 3**, el peor caso es **Instagram con 12,06%** de error mediano — las otras tres plataformas están muy por debajo: Facebook 2,12%, TikTok 5,94%, Twitter/X 0,38%. Suficientemente preciso para construir el dataset de entrenamiento.

---

## BLOQUE 7 — Etapa 3: Colombia, ELA-NOM paso a paso (10 min)

*[Diapositiva 15: universo y filtros]*

### Universo y filtros

Partimos de las **33 ciudades más pobladas** de Colombia. Se excluyeron dos con criterios explícitos: Bogotá, porque uno de sus candidatos tiene audiencia internacional que rompe el supuesto de localidad geográfica del modelo; y Piedecuesta, porque el candidato ganador eliminó sus perfiles durante la campaña por procesos legales. Resultado: **31 ciudades competitivas**.

Dentro de cada ciudad, solo candidatos con **más de 10.000 votos confirmados**. Este umbral elimina candidaturas sin campaña digital activa real. Su consecuencia metodológica — reconocida explícitamente en la tesis — es que introduce un **sesgo de selección sobre la variable dependiente**: las métricas reportadas reflejan el subconjunto más predecible del panel.

El resultado: **120 candidatos**, con el **92,6%** con publicaciones activas en al menos una plataforma.

*[Diapositiva 16: infraestructura de extracción]*

### Qué se extrajo y cómo

La extracción cubrió **tres plataformas**: Facebook, TikTok y Twitter/X. Instagram quedó excluido: Meta cerró su API para investigadores independientes en 2023.

Para Twitter/X: scraper propio con **Playwright** (navegador headless). Para Facebook y TikTok: **Apify** (infraestructura comercial de scraping). La ventana: **14 días anteriores al 29 de octubre de 2023**.

En total: **5.776 publicaciones únicas** — 2.511 de Facebook, 2.346 de Twitter/X, 919 de TikTok.

*[Diapositiva 17: señal Colombia — P1]*

### Verificación de la señal — P1

Antes de modelar, verificamos que la señal existiera. Una prueba **U de Mann-Whitney** sobre el engagement por publicación mostró que los ganadores tienen significativamente más interacciones que los perdedores: **p = 0,0481**.

Los **120 candidatos no son observaciones independientes** — están anidados en 31 contiendas. Para validar el resultado respetando esa estructura, se realizó un **test de permutación intra-contienda**: se mezclaron 10.000 veces las etiquetas ganador/perdedor *dentro* de cada municipio y se midió cuántas permutaciones superaban el estadístico observado. El estadístico observado fue una diferencia de medianas de **112 puntos de engagement**. Ninguna de las 10.000 permutaciones igualó ese valor: **p-valor empírico menor que 0,0001**. El resultado confirma que la diferencia es genuina, no un artefacto de la estructura de anidamiento.

La correlación de Spearman entre la dominancia de likes y la cuota de voto fue **ρ = 0,70**. Cuantificamos la composicionalidad mediante permutación de likes dentro de cada contienda: el componente mecánico es **ρ_mec = 0,261 (39%)**, y la señal predictiva real es **ρ_real ≈ 0,41 (61%)**, con p menor que 0,0001 (ninguna de las 10.000 permutaciones alcanzó el ρ observado). La validez predictiva real se establece por LOCO-CV, no por el ρ descriptivo.

Un clasificador que asigne la victoria al candidato con mayor volumen bruto acertaría en el **57,6%** de las contiendas. Con **dominancia relativa** — cuota de likes de cada candidato sobre el total — ese porcentaje sube al **71,0%**. La dominancia relativa es más informativa que el volumen absoluto.

La señal existe. Esto responde **P1**.

*[Diapositiva 18: normalización y familias de variables]*

### Construcción del dataset y normalización

Con el restaurador Weibull, las interacciones brutas de cada publicación se convirtieron en **estimaciones del estado al día de la elección** — descuentando el tráfico póstumo acumulado entre octubre 2023 y la fecha de extracción.

A partir de esas interacciones reconstruidas se generó un pool inicial de **más de 22 variables**, derivadas de tres familias:

**Interacciones nominales absolutas**: likes, comentarios y compartidos totales por plataforma. Capturan el volumen bruto de actividad. Útiles pero ruidosas: un candidato que publica más naturalmente acumula más.

**Interacciones por publicación**: likes, comentarios y compartidos promedio por post. Normalizan por la actividad editorial del candidato. Más estables que las nominales, pero siguen dependiendo del tamaño absoluto de la contienda.

**Dominancia relativa**: la cuota de likes de un candidato sobre el total de la contienda. Elimina el efecto del tamaño absoluto y mide la señal competitiva directamente. Es la variable más informativa, como confirman el clasificador naive (71%) y la correlación Spearman (ρ=0,70 vs ρ=0,45 del volumen absoluto).

Se intentó también normalizar por número de seguidores, con la intuición de que candidatos con más seguidores naturalmente acumulan más interacciones. Sin embargo, el número de seguidores resultó ser inestable, altamente colineal con el volumen de publicaciones y no disponible históricamente en todas las plataformas. VIF elevado lo descartó del pool.

*[Diapositiva 19: feature engineering y selección del modelo]*

### Feature engineering: de 22 a 9, de 9 a 2

Un análisis de **factor de inflación de la varianza (VIF)** reveló multicolinealidad extrema entre las variables brutas. Se consolidó el pool a **9 variables conceptualmente distinguibles**:

- **6 cuotas digitales en logit:** dominancia de likes, comentarios y compartidos; y likes, comentarios y compartidos promedio por publicación.
- **2 variables territoriales:** logaritmo de la población y número de candidatos.
- **1 moderador de interacción:** logit(dominancia likes) × (log-población centrada en su media).

La transformación al logit es natural: la variable dependiente — la cuota de voto — está acotada en (0,1) y el logit lleva ambas a la escala log-odds, donde la relación tiende a ser más lineal.

El moderador captura si el efecto de la señal digital varía según el tamaño de la ciudad. La centración del log-población en su media hace que β₀ sea interpretable: la cuota predicha para el candidato promedio en la ciudad promedio. En ciudades grandes, la señal digital pesa más; en ciudades pequeñas, las redes de contacto personal pueden compensarla.

### AutoML y selección del modelo

Se evaluaron sistemáticamente múltiples familias de modelos — GLM fraccional, gradient boosting, redes neuronales, random forests, SVM — todos bajo la misma validación LOCO-CV. El **GLM fraccional con regularización ElasticNet** fue el mejor.

¿Por qué el GLM sobre gradient boosting, que alcanzó un MAE similar de 9,91 pp? Dos razones. Primera, teórica: la cuota de voto está en (0,1) y el GLM fraccional — propuesto por Papke y Wooldridge en 1996 — respeta esos límites con familia binomial y link logit. Segunda, práctica: una tesis académica requiere interpretabilidad. Los coeficientes del GLM tienen lectura directa en log-odds; el gradient boosting es una caja negra.

El **ElasticNet** combina Lasso (L₁) y Ridge (L₂). Lasso ajusta algunos coeficientes a exactamente cero — selección automática de variables. Ridge contrae suavemente los restantes ante multicolinealidad. La calibración fue **anidada**: un CV interno eligió alpha=0,0475 y L1-ratio=0,10 *antes* de ver el pliegue de evaluación. Un CV externo LOCO midió el desempeño real.

*[Diapositiva 20: LOCO-CV — la validación honesta]*

### LOCO-CV: la validación honesta

**LOCO-CV** — *Leave-One-Contest-Out Cross-Validation* — es el método de validación central del estudio. La alternativa estándar, mezclar candidatos aleatoriamente entre entrenamiento y prueba, generaría fuga de información: las cuotas de likes y votos de una misma contienda suman 1 por definición, por lo que ver candidatos de la misma ciudad en entrenamiento y en prueba filtraría información composicional directa.

El proceso opera en **dos fases**. En la **Fase 1** (evaluación honesta), se hace un ciclo de 31 pliegues externos. En cada pliegue se bloquea una ciudad completa como conjunto de prueba. Dentro del pliegue, un grid search interno evalúa 120 combinaciones de alpha y l1_ratio sobre las 30 ciudades de entrenamiento, sin acceder a la ciudad bloqueada. La combinación ganadora entrena el ElasticNet definitivo de ese pliegue, que predice la ciudad bloqueada. El MAE es el promedio de los 31 errores. En la **Fase 2** (modelo final), los hiperparámetros más frecuentes — alpha = 0,0475, l1_ratio = 0,10 — se usan para entrenar sobre las 31 ciudades completas, produciendo los coeficientes definitivos.

El resultado: **MAE = 9,56 pp** y **R²oos = 0,518**.

*[Diapositiva 21: especificación ganadora e interpretación]*

### La especificación ganadora y la interpretación de los betas

El ElasticNet seleccionó **dos variables** del pool de nueve:

$$\hat{y}_c = 0{,}258 + 0{,}111 \cdot f_{\ell} + 0{,}026 \cdot (f_{\ell} \times (\ln\text{pob} - \overline{\ln\text{pob}}))$$

donde $f_{\ell}$ es el logit de la dominancia de likes.

Las siete variables restantes fueron contraídas a cero: su contribución marginal al MAE fuera de muestra era negativa.

¿Cómo se leen los coeficientes?

- **β₀ = 0,258**: la cuota predicha para el candidato promedio en la ciudad promedio. Es consistente con 3,84 candidatos por contienda: 1/3,84 ≈ 26%.

- **β₁ = 0,111**: por cada unidad adicional en el logit de la dominancia de likes, la cuota en log-odds sube 0,111. En términos prácticos: pasar del 25% al 50% de dominancia digital corresponde a un incremento en logit de ≈1,1 unidades, lo que se traduce en ≈10 pp adicionales de cuota predicha.

- **β₂ = 0,026**: el moderador. En ciudades grandes (log-pob por encima de la media), el efecto total de la señal es β₁ + β₂ × desviación. Dominar las redes sociales pesa más electoralmente en ciudades grandes.

*[Diapositiva 22: dos modelos — reconciliación de coeficientes]*

### Por qué hay dos modelos y cuál se usa en 2026

El proceso produjo dos especificaciones con desempeño prácticamente idéntico: la de **2 predictores** (MAE=9,56 pp) y la del **pool completo de 9 variables** (MAE=9,57 pp).

El modelo de 9 variables retiene como predictores directos el número de candidatos y el log-población. En una segunda vuelta presidencial, el número de candidatos es siempre exactamente 2 — es una constante sin poder discriminador. El modelo de 2 predictores retiene solo señal digital pura y su interacción con la población, que tienen sentido conceptual tanto con 2 como con 10 candidatos.

Para la segunda vuelta de 2026 se usó la especificación de 2 predictores, re-centrando el intercepto sobre el **50%** de base:

$$\hat{p}_c^{(2)} = 0{,}50 + (\hat{\boldsymbol{\beta}} \cdot \mathbf{x}_c)$$

La dominancia de likes en logit es el predictor más robusto y parsimonioso. Esto responde **P3**.

*[Diapositiva 23: curva de aprendizaje — P4]*

### ¿Cuántas contiendas se necesitan? — P4

La curva de aprendizaje muestra una reducción de apenas **0,77 pp** entre 5 y 30 ciudades. Con **10 ciudades** se alcanza el **95% del rendimiento final**. El piso de error lo determina el ruido intrínseco de la señal digital, no la insuficiencia de datos. El modelo es viable desde muestras moderadas.

Esto responde **P4**.

---

## BLOQUE 8 — Validación prospectiva: segunda vuelta 2026 (3 min)

*[Diapositiva 24: validación prospectiva 2026]*

El **21 de junio de 2026**: Iván Cepeda Castro contra Abelardo De la Espriella.

El modelo entrenado en **31 elecciones de alcaldes** se aplicó **sin reentrenamiento** a una elección presidencial bipolar nacional. **444 publicaciones** en total. Cepeda acumuló **17.087.679 likes** (dominancia **77,6%**); De la Espriella, **4.926.361** (dominancia **22,4%**).

Pronóstico: **Cepeda 60,5% — De la Espriella 39,5%**.

*[Diapositiva 25: resultado real y contextualización]*

Resultado real: De la Espriella ganó por **0,96 pp**: **50,48% vs. 49,52%**. MAE del modelo: **10,98 pp** — 1,42 pp por encima del MAE de referencia de 9,56 pp.

La señal digital de Cepeda era real: 3,5 veces más likes. Pero el margen real fue de menos de un punto porcentual — inferior al propio error del modelo. En contiendas de empate técnico, ningún sistema basado en engagement tiene la resolución necesaria para determinar el ganador. El uso adecuado de ELA-NOM es detectar tendencias y ventajas claras superiores a 20 pp, no predecir con precisión contiendas de empate.

Esto responde **PM4**: el modelo es transferible a un formato electoral diferente sin reentrenamiento.

---

## BLOQUE 9 — Conclusiones (2 min)

*[Diapositiva 26: conclusiones — respuesta a la pregunta central]*

¿Es posible?

**Sí. Con matices estructurales bien documentados.**

Las ocho preguntas respondidas: PM1 y PM2 en Bolivia; P2 y PM3 en Costa Rica; P1, P3 y P4 en Colombia; PM4 con la validación 2026.

**MAE = 9,56 pp fuera de muestra** en 31 contiendas. R²oos = 0,518. El modelo se transfiere a un formato electoral diferente. El restaurador Weibull resuelve el problema del histórico. Todo esto con una inversión de entre **20 y 30 dólares**.

*[Diapositiva 27: cuatro contribuciones al estado del arte]*

Las cuatro contribuciones al estado del arte:

1. **Elección-agnosticismo empírico**: primera ruta metodológica demostrada para superar la no-transferibilidad del SOMEN-DC.
2. **Independencia demoscópica total**: modelo que ancla la optimización sobre el escrutinio final — el único ground truth universal.
3. **Restaurador temporal Weibull**: arquitectura matemática para construir datasets históricos desde una extracción estática.
4. **Democratización del pipeline**: todo el ciclo por 20–30 USD.

*[Diapositiva 28: próximos pasos y agenda futura]*

El juicio definitivo llega con las **elecciones territoriales de Colombia en 2027**: modelo ya entrenado, evaluación ex-ante estricta. La extensión más valiosa: **nowcasting continuo diario** durante la campaña — la arquitectura técnica ya está resuelta.

*[Diapositiva 29: cumplimiento de objetivos específicos]*

*[Diapositiva 30: cierre]*

**Muchas gracias.**

---

## TABLA DE TIEMPOS

| Bloque | Contenido | Tiempo |
|---|---|---|
| Saludo | Presentación formal | 0,5 min |
| 1 | El problema | 2 min |
| 2 | Literatura | 2 min |
| 3 | Pregunta de investigación | 1,5 min |
| 4 | Objetivos | 0,5 min |
| 5 | Bolivia | 4 min |
| 6 | Costa Rica | 4,5 min |
| 7 | Colombia (extracción, normalización, feature eng., AutoML, LOCO-CV, dos modelos) | 10 min |
| 8 | Validación 2026 | 3 min |
| 9 | Conclusiones | 2 min |
| **Total** | | **~30 min** |

---

## NOTAS PARA EL PRESENTADOR — PREGUNTAS PROBABLES DEL JURADO

> Las preguntas marcadas con 🔴 son **Prioridad 1** — casi seguro van a aparecer. Las marcadas con 🟡 son **Prioridad 2** — pueden aparecer como seguimiento.

---

### 🔴 PRIORIDAD 1

**🔴 "Encontramos tres juegos de coeficientes distintos para el mismo modelo"**
> Los tres corresponden a tres especificaciones distintas: (1) β₁=0,111 y β₂=0,026 — modelo de 2 predictores, los definitivos. (2) β_mod=0,557 — ElasticNet sobre el pool completo de 9 variables. (3) β≈0,423 — regresión fraccional simple de la Sección 5.6.a. La tesis tiene una tabla unificada de reconciliación.

**🔴 "¿Cuál modelo se aplicó en 2026 y de qué modelo es el MAE=9,56?"**
> El modelo de 2 predictores, ElasticNetCV(random_state=42), StandardScaler, sobre las 31 contiendas colombianas. El MAE de 9,56 pp es de ese modelo bajo LOCO-CV. El 9,57 pp pertenece al pool completo de 9 variables — especificaciones distintas con resultados prácticamente idénticos.

**🔴 "El ±MAE no es un intervalo de predicción formal"**
> Correcto. El MAE es exactitud promedio, no dispersión. Esa construcción fue corregida en la tesis. Lo que decimos ahora: el resultado real de 49,52% supera el límite de referencia heurística en 1,42 pp. Un intervalo formal requeriría supuestos distribucionales adicionales.

**🔴 "El filtro de 10.000 votos crea sesgo de selección sobre la variable dependiente"**
> Es una limitación real, reconocida explícitamente. Las métricas reportadas reflejan el subconjunto más predecible. Esta limitación es inherente al diseño en ausencia de un criterio de exclusión que no dependa de los resultados.

**🔴 "¿Qué hicieron con los candidatos sin publicaciones donde el logit no está definido?"**
> Se imputó dominancia mínima ε=10⁻³ (0,1%), produciendo logit(0,001)≈−6,91. Análisis de sensibilidad: con ε=1% el valor sería −4,60, una diferencia de 2,31 unidades-logit que × β=0,111 desplazaría la predicción ≈26 pp. Los candidatos afectados (~9 de 120) son los menos votados y ElasticNet los penaliza fuertemente.

---

### 🟡 PRIORIDAD 2

**🟡 "Los parámetros Weibull están mal interpretados"**
> En F(t)=1−e^(−k(t+t₀)^α): k es una tasa (no escala clásica). α controla la geometría: α<1 desacelera; α>1 la tasa crece — Twitter/X con α=1,14 refleja acumulación acelerada (retweet). t₀ es un adelanto de origen: hace que F(0)>0, modelando interacciones previas al primer día de observación.

**🟡 "Mann-Whitney asume independencia; el Spearman de 0,70 es composicional"**
> p=0,0481 es del engagement por publicación. La estructura de anidamiento se valida con test de permutación intra-contienda. El Spearman es evidencia exploratoria; la validez predictiva real se establece por LOCO-CV. El ρ≈0,45 del volumen absoluto confirma que la dominancia es más informativa.

**🟡 "¿Por qué el Top-1 baja al 64,5% si el baseline está en 71%?"**
> Minimizar MAE de magnitud y maximizar exactitud de clasificación ordinal son objetivos distintos. El modelo sacrifica exactitud de ranking a cambio de estimaciones de magnitud más calibradas.

**🟡 "¿Cómo se controla el sobreajuste y por qué LOCO-CV es validación real?"**
> Dos niveles: (1) CV interno elige hyperparámetros antes de ver el pliegue. (2) LOCO-CV externo mide MAE sobre la ciudad excluida completa. La aplicación a 2026 es un tercer nivel: fuera de muestra en formato de elección. Repositorio público: código, versiones de librerías, random_state=42.

**🟡 "¿Qué mide realmente el modelo — intención de voto o cuota electoral?"**
> ELA-NOM aproxima la cuota electoral observada, no la intención de voto latente. El proxy digital puede capturar apoyo genuino, visibilidad, polarización y pauta paga simultáneamente. El único claim predictivo: cuota de likes predice cuota de votos con MAE=9,56 pp fuera de muestra.

**🟡 "El OE4 anuncia clasificación Y regresión, pero solo hay regresión"**
> El Top-1 del 64,5% es una métrica derivada de la regresión, no un clasificador entrenado independientemente. El OE4 fue reformulado en la tesis. Un logit condicional de McFadden queda como trabajo futuro.

---

### ⚪ OTRAS PREGUNTAS PROBABLES

**"¿Por qué excluir Instagram de Colombia?"** Meta cerró su API para investigadores independientes en 2023. Restricción externa del ecosistema.

**"El error en 2026 fue de 10,98 pp — ¿no invalida el modelo?"** El MAE medio es 9,56 pp. El margen real fue de 0,96 pp — inferior al propio error. Ningún modelo de engagement puede resolver un empate técnico.

**"¿El R² del Weibull es muy bajo?"** El 66,8% de la varianza es ruido intra-publicación irreducible. El modelo captura la forma global de la curva, que es lo que necesita para la reconstrucción.

**"¿Por qué no normalizar por seguidores?"** El número de seguidores es inestable, altamente colineal con el volumen de publicaciones y no disponible históricamente en todas las plataformas. VIF elevado lo descartó.

**"¿Por qué la dominancia relativa y no el volumen absoluto?"** Clasificador naive: dominancia 71% vs volumen bruto 57,6%. Spearman: ρ=0,70 vs ρ≈0,45. La dominancia elimina el efecto del tamaño de la contienda y mide la señal competitiva directamente.

**"¿Cuánto cuesta replicar esto?"** Entre 20 y 30 dólares en créditos de Apify. Procesamiento corre en cualquier computador con Python.
