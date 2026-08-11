# Pipeline Colombia 2023: Explicación paso a paso
## Documento de apoyo para la defensa: ELA-NOM

---

## PASO 1: Definición del universo

**Universo inicial:** 33 ciudades más pobladas de Colombia.

**Exclusiones con criterio explícito (2 ciudades):**

- **Bogotá:** Gustavo Bolívar, escritor con audiencia latinoamericana, acumuló millones de interacciones siendo tercer lugar. Viola el supuesto de localidad geográfica: la mayoría de sus likes no provienen de electores bogotanos. Su inclusión habría roto la función de mapeo del modelo.
- **Piedecuesta:** el candidato ganador eliminó voluntariamente sus perfiles durante la campaña por procesos legales. Imposible reconstruir su señal digital.

**Resultado: 31 ciudades competitivas.**

**Filtro de candidatos: más de 10.000 votos confirmados en escrutinios.**

Objetivo: eliminar candidaturas testimoniales sin campaña digital activa. De los 328 candidatos totales, 120 superaron el umbral.

> **Advertencia metodológica documentada en la tesis:** este filtro introduce un sesgo de selección sobre la variable dependiente. Se excluye exactamente a los peor votados, haciendo el dataset más predecible de lo que sería en la práctica real. Las métricas reportadas (MAE = 9,56 pp, R2oos = 0,518) reflejan ese subconjunto, no el universo completo.

**Imputación epsilon:** aproximadamente 9 candidatos no tenían ninguna publicación. Para evitar logit(0) = -infinito, se imputó dominancia = 0,001 (epsilon = 10^-3), lo que da logit(0,001) = -6,91. Con epsilon = 0,01 el logit sería -4,60, una diferencia de 2,31 unidades que multiplicada por beta_1 = 0,111 desplazaría la predicción 26 pp. Por eso declarar el valor de epsilon es esencial para la replicabilidad.

---

## PASO 2: Scraping

**Ventana:** 14 dias previos al 29 de octubre de 2023.

**Tres infraestructuras paralelas:**

| Plataforma | Herramienta | Razon |
|---|---|---|
| Twitter/X | Playwright (navegador headless automatizado) | API de pago desde 2023 |
| Facebook | Apify (API privada no documentada de Meta) | API Graph cerrada |
| TikTok | Apify | Sin API publica disponible |
| Instagram | EXCLUIDA | Meta bloqueo acceso investigadores en 2023 |

**Resultado bruto: 5.776 publicaciones unicas** (FB: 2.511, TW: 2.346, TikTok: 919).

---

## PASO 3: Restauracion Weibull

Las interacciones extraidas en 2026 reflejan 3 anos de trafico acumulado, no el estado del dia de la eleccion. Se aplico la funcion calibrada en Costa Rica:

```
N_estimado = n_hoy / F(t; k, alpha, t0)
```

donde `t` es el numero de dias entre la publicacion y la extraccion, y `F` es la Weibull calibrada por plataforma. Esto convirtio cada publicacion en una estimacion de cuantas interacciones tenia el 29 de octubre de 2023.

Los parametros exportados desde Costa Rica se aplicaron directamente, sin recalibrar, validando la transferibilidad del restaurador.

---

## PASO 4: Validacion de la senal (ANTES del modelado)

### Mann-Whitney mancomunado

Se comparo el engagement por publicacion de ganadores vs. perdedores:

- **Mediana ganadores:** 204 eng/publicacion
- **Mediana perdedores:** 92 eng/publicacion
- **Estadistico U:** 2.293,5
- **p-valor (unilateral):** 0,0481

El p-valor de 0,0481 corresponde a la comparacion de la mediana de engagement por publicacion (no del total bruto). El total bruto (44.252 vs. 28.011) no es la estadistica reportada.

### Test de permutacion intra-contienda

**Por que es necesario:** Mann-Whitney asume que los 120 candidatos son observaciones independientes. Pero estan anidados en 31 contiendas: los 4 candidatos de Medellin compiten entre si y sus datos estan correlacionados. Mann-Whitney podria ver un efecto que en realidad es un artefacto del anidamiento.

**Como funciona (10.000 iteraciones, semilla = 42):**

1. Se calcula el estadistico observado: diferencia de medianas de engagement entre ganadores y perdedores = **112 puntos de engagement**.
2. En cada iteracion: se barajan aleatoriamente las etiquetas "ganador"/"perdedor" DENTRO de cada municipio por separado. Los candidatos de Medellin solo se intercambian entre si; los de Cali, entre si; etc.
3. Se recalcula la diferencia de medianas en cada permutacion.
4. p-valor empirico = fraccion de iteraciones que igualaron o superaron el estadistico observado.

**Resultados:**

| Dato | Valor |
|---|---|
| Estadistico observado (delta mediana) | 112,0 |
| Media de delta mediana bajo H0 | -0,52 |
| Percentil 95 bajo H0 | 39,0 |
| Percentil 99 bajo H0 | 76,0 |
| **p-valor empirico** | **menor que 0,0001** (0 de 10.000 permutaciones igualaron o superaron 112) |

**Interpretacion:** el valor observado de 112 es tan extremo que ninguna de las 10.000 configuraciones aleatorias lo alcanzo. Esto confirma que la senal no es un artefacto del anidamiento.

**Que significa exactamente delta = 112 eng/pub:**
- **delta:** diferencia entre los dos grupos (ganadores menos perdedores)
- **tilde{x}:** se usa la mediana (no la media), que es mas robusta a outliers
- **eng:** engagement = suma de likes + comentarios + compartidos
- **pub:** por publicacion (por post)
- **Traduccion:** la mediana de engagement por publicacion de los candidatos ganadores supera en 112 unidades la de los perdedores. Si el ganador tipico tiene 204 eng/pub y el perdedor tipico tiene 92, la diferencia es 112.
- **Por que mediana y no media:** la media total (44.252 vs 28.011) viene del Mann-Whitney mancomunado y refleja diferencias de tamano de campana. Al dividir por publicaciones y usar la mediana se neutralizan los extremos (un post viral aislado no infla el estadistico). El test de permutacion usa la diferencia de medianas porque es la mas resistente a ese tipo de ruido.

### Correlaciones de Spearman

| Variable X | rho | p-valor | Interpretacion |
|---|---|---|---|
| Dominancia relativa de likes | 0,70 | menor que 0,001 | Cuota digital predice cuota electoral |
| Volumen absoluto de likes | aprox. 0,45 | menor que 0,001 | Menos informativo (sin normalizar) |

La diferencia entre 0,70 y 0,45 es el argumento empirico central de por que el modelo usa dominancia relativa y no volumen bruto.

> **Advertencia composicional:** dominancia y cuota de votos son variables composicionales (ambas suman 1 por contienda). Eso infla mecanicamente la correlacion. El rho de 0,70 es evidencia exploratoria/descriptiva; la validez predictiva real se establece por LOCO-CV.

### Heuristico de dominancia

Asignar la victoria al candidato con mayor dominancia de likes acierta en **22 de 31 contiendas = 71,0%** (IC 95% Wilson: 53,4% a 83,9%).

Progresion que justifica usar dominancia relativa:
- Azar puro (1/3,84 candidatos): 26,0%
- Volumen absoluto (mas likes brutos = ganador): 57,6%
- Dominancia relativa (mayor cuota digital = ganador): **71,0%**

---

## PASO 5: Normalizacion y construccion de variables

Con las interacciones restauradas se construyo un pool de mas de 22 variables en tres familias:

**Familia 1: Nominales absolutas**
Likes, comentarios y compartidos totales por plataforma. Capturan volumen bruto. Problema: quien mas publica naturalmente acumula mas. Senal ruidosa y dependiente de la frecuencia editorial.

**Familia 2: Por publicacion**
Likes, comentarios y compartidos promedio por post. Normalizan la actividad editorial. Mas estables, pero siguen dependiendo del tamano absoluto de la contienda.

**Familia 3: Dominancia relativa** (la elegida)
Cuota de likes de un candidato sobre el total de su contienda. Elimina el efecto del tamano absoluto y mide la senal competitiva directamente.

**Transformacion logit:** todas las dominancias se transforman al logit porque la variable dependiente (cuota de voto) esta acotada en (0,1) y la relacion logit-logit tiende a ser mas lineal.

**Intento descartado: normalizar por seguidores**
VIF elevado. El numero de seguidores es inestable entre plataformas, colineal con el volumen de publicaciones, y no estaba disponible historicamente en todas las plataformas. Se descarto del pool.

---

## PASO 6: Reduccion VIF (22+ variables a 9)

El VIF (Factor de Inflacion de la Varianza) de una variable X_j se calcula:

1. Regresar X_j contra todas las demas variables del pool
2. Obtener el R2 de esa regresion
3. VIF_j = 1 / (1 - R2_j)

Un VIF alto significa que esa variable es casi redundante: ya esta contenida en las demas. Con VIF alto, los coeficientes de una regresion OLS se vuelven inestables (pequenos cambios en datos producen cambios enormes en coeficientes).

**Umbral convencional:** VIF mayor que 5 es preocupante; mayor que 10 es severo.

**Los VIFs reales de las 6 variables digitales (datos del notebook 04_automl_seleccion.ipynb):**

| Variable | VIF | Nivel |
|---|---|---|
| f_coment_dom (dominancia comentarios) | 351,6 | Extremo |
| f_coment_pp (comentarios por publicacion) | 265,2 | Extremo |
| f_likes_dom (dominancia likes) | 225,4 | Extremo |
| f_likes_pp (likes por publicacion) | 158,9 | Extremo |
| f_compart_dom (dominancia compartidos) | 126,5 | Extremo |
| f_compart_pp (compartidos por publicacion) | 92,4 | Extremo |

**Por que son tan altos:** si un candidato tiene muchos likes, tiende a tener muchos comentarios y muchos compartidos. Las 6 variables se mueven casi en bloque.

**Consecuencia:** una regresion OLS con estas 6 variables daria coeficientes completamente inestables. La solucion correcta no es podar variables manualmente sino usar regularizacion que tolere la colinealidad: **ElasticNet**.

**Las 9 variables del pool se definieron por criterio conceptual,** no por un umbral VIF automatico:

| # | Variable | Familia |
|---|---|---|
| 1 | logit(dominancia likes) | Digital |
| 2 | logit(dominancia comentarios) | Digital |
| 3 | logit(dominancia compartidos) | Digital |
| 4 | logit(likes por publicacion) | Digital |
| 5 | logit(comentarios por publicacion) | Digital |
| 6 | logit(compartidos por publicacion) | Digital |
| 7 | log(poblacion del municipio) | Territorial |
| 8 | numero de candidatos en la contienda | Territorial |
| 9 | logit(dom. likes) x (log-pob centrada en su media) | Moderador |

El moderador (variable 9) captura si el efecto de la dominancia digital varia segun el tamano de la ciudad. La centracion en la media hace que beta_0 sea interpretable: la cuota predicha para el candidato promedio en la ciudad promedio.

---

## PASO 7: AutoML acotado - comparacion de modelos

Se probaron multiples especificaciones de variables y multiples familias de modelos. Todo bajo la misma metrica (MAE fuera de muestra) y el mismo protocolo de validacion (LOCO-CV).

**Reglas del proceso (extraidas del notebook, celda 0):**
1. Todo se mide fuera de muestra con LOCO-CV. Nada se decide por ajuste en entrenamiento.
2. Metrica unica: MAE de la cuota de voto en puntos porcentuales.
3. La regularizacion hace la poda, no el investigador.
4. La seleccion es anidada: CV interno elige hiperparametros, CV externo mide el desempeno real.

**Especificaciones de variables evaluadas (datos reales del notebook):**

| Especificacion | Variables | MAE (pp) | R2oos | Top-1 |
|---|---|---|---|---|
| likes + territorio | 3 | 10,37 | 0,507 | 71,0% |
| likes + moderador(pob) | 2 | 10,37 | 0,506 | 71,0% |
| Dominancia + territorio | 5 | 10,69 | 0,472 | 64,5% |
| Todo digital + territorio | 8 | 10,73 | 0,455 | 54,8% |
| Solo likes_dom | 1 | 11,54 | 0,457 | 71,0% |
| Dominancia + por_post | 6 | 11,66 | 0,424 | 61,3% |
| Dominancia (3 variables) | 3 | 11,81 | 0,422 | 67,7% |
| Por_post (3 variables) | 3 | 11,97 | 0,409 | 58,1% |
| Baseline proporcionalidad | 0 | 12,64 | 0,180 | 71,0% |

**Observacion clave:** usar 8 variables da peor MAE (10,73) que usar 3 (10,37). Mas variables sobreajustan. El modelo necesita parsimonia.

**Familias de modelos evaluadas:**
- GLM fraccional (Papke y Wooldridge, 1996)
- Gradient boosting (HistGradientBoosting)
- Redes neuronales
- Random forests
- SVM

**Ganador: GLM fraccional con ElasticNet.**

**Por que GLM sobre gradient boosting (MAE similar: 9,91 pp)?**
1. *Teorica:* la cuota de voto esta en (0,1). El GLM fraccional con familia binomial y link logit garantiza que todas las predicciones caen en (0,1). OLS puede predecir valores negativos o mayores que 1. Gradient boosting tampoco garantiza ese rango sin ajustes adicionales.
2. *Practica:* una tesis academica requiere interpretabilidad. Los coeficientes del GLM tienen lectura directa en log-odds. Gradient boosting es una caja negra.

---

## PASO 8: ElasticNet anidado - seleccion de variables

**Que hace ElasticNet:** combina Lasso (L1) y Ridge (L2).
- **Lasso (L1):** ajusta algunos coeficientes a exactamente cero. Seleccion automatica de variables.
- **Ridge (L2):** contrae suavemente los restantes ante multicolinealidad.

La funcion de perdida minimizada:
```
min_beta { L_fraccional(beta) + alpha * [gamma * ||beta||_1 + (1-gamma)/2 * ||beta||_2^2] }
```

Hiperparametros optimos calibrados: alpha = 0,0475, gamma (l1_ratio) = 0,10.

**La calibracion fue anidada (dos niveles):**

- **CV interno:** en cada pliegue LOCO, se corre un CV adicional sobre las 30 ciudades de entrenamiento para elegir alpha y gamma. Este CV interno nunca ve la ciudad excluida.
- **CV externo (LOCO):** mide el MAE real sobre la ciudad excluida, que el modelo nunca vio.

**Por que importa el anidamiento:** si eligieras los hiperparametros mirando el MAE fuera de muestra directamente, estarias usando informacion del test para tomar decisiones de entrenamiento. Eso infla artificialmente el desempeno reportado.

**Estabilidad de seleccion por variable (datos reales del notebook):**

| Variable | % de pliegues donde sobrevivio | Coeficiente medio |
|---|---|---|
| logit(dom. likes) | 100% | 0,375 |
| log(poblacion) | 100% | 0,201 |
| moderador likes x pob | 100% | 0,557 |
| n_candidatos | 100% | -0,396 |
| logit(likes por pub) | 97% | 0,137 |
| logit(dom. comentarios) | 94% | 0,095 |
| logit(compart. por pub) | 87% | 0,039 |
| logit(dom. compartidos) | 77% | 0,081 |
| logit(coment. por pub) | 10% | 0,004 |

**MAE con el pool completo de 9 (ElasticNet anidado): 9,61 pp** (casi identico al MAE de la especificacion final de 2 variables).

La especificacion final reportada uso 2 predictores (MAE = 9,56 pp) vs. la de 9 (MAE = 9,57 pp): diferencia de 0,01 pp, indistinguible empiricamente. Se eligio la de 2 por mayor parsimonia e interpretabilidad.

---

## PASO 9: LOCO-CV - validacion honesta

**Leave-One-Contest-Out Cross-Validation: 31 pliegues.**

**Por que no K-Fold estandar:** K-Fold mezcla candidatos aleatoriamente. Podria poner candidatos de Medellin en entrenamiento y en prueba simultaneamente. El modelo aprenderia patrones especificos de esa ciudad y los "reutilizaria" en la evaluacion, produciendo estimaciones artificialmente optimistas. Con variables composicionales (cuotas que suman 1 dentro de cada contienda), esto genera fuga de informacion directa.

---

### Explicacion paso a paso del proceso completo

**Datos de entrada:** 9 variables (con logit aplicado) para 120 candidatos de 31 ciudades.

**FASE 1 — Evaluacion honesta:**

Realizo un ciclo for de 31 folds. En el fold 1, escojo 30 ciudades de entrenamiento y bloqueo la ciudad 31 completamente: no la toco para nada hasta el final del fold.

Dentro de ese fold, hago un grid search: selecciono la primera de las 120 combinaciones de alpha y l1_ratio y entreno el ElasticNet con esas 30 ciudades. Para medir si esa combinacion es buena, no uso la ciudad 31 (esta bloqueada). Hago un mini-ciclo interno de 30 folds sobre esas mismas 30 ciudades: entreno con 29, predigo la que sobro, repito para cada ciudad. El promedio de esos 30 errores es el MAE interno de esa combinacion. Repito esto para las 119 combinaciones restantes. Me quedo con la combinacion que tuvo el menor MAE interno.

Con esa combinacion ganadora, entreno el ElasticNet sobre las 30 ciudades completas. El proceso puede dejar las 9 variables, puede bajarlas a 2 o a cualquier numero: depende de la penalizacion. En la practica, en la mayoria de los folds quedaron 2.

Ahora desbloqueo la ciudad 31 y predigo su cuota electoral. Calculo el error para ese fold y lo guardo.

Paso al fold 2, hago exactamente lo mismo: grid search interno completo, nuevo modelo, predigo la ciudad 2. Y asi hasta el fold 31.

Al final tengo 31 errores. Los promedio: **MAE = 9,56 pp**. Tambien se cual combinacion de hiperparametros gano mas veces: alpha = 0,0475 y l1_ratio = 0,10. Termina la Fase 1.

**FASE 2 — Modelo final:**

Tomo la combinacion ganadora y entreno el ElasticNet una ultima vez sobre las 31 ciudades completas, sin dejar ninguna afuera, porque ya no necesito medir error (ya lo medi en la Fase 1). Los betas que salen de ese entrenamiento final, promediados y estandarizados a traves de los 31 folds, son **beta_0 = 0,258, beta_1 = 0,111 y beta_2 = 0,026**. Ese es el modelo que se aplica en 2026.

---

**Resultados LOCO-CV:**

| Metrica | Valor |
|---|---|
| MAE fuera de muestra | **9,56 pp** |
| R2 fuera de muestra | **0,518** |
| Top-1 (clasificacion derivada) | **64,5%** |
| MAE baseline proporcionalidad | 12,61 pp |
| Mejora sobre baseline | 3,05 pp |

**Por que el Top-1 baja de 71% a 64,5%:** minimizar MAE de magnitud y maximizar exactitud de clasificacion ordinal son objetivos distintos. El modelo sacrifica precision de ranking a cambio de estimaciones de magnitud mas calibradas. El Top-1 del 64,5% es una metrica derivada de la regresion, no un clasificador entrenado independientemente.

---

## PASO 10: Ecuacion final e interpretacion de coeficientes

La especificacion ganadora:

```
y_hat_c = 0,258 + 0,111 * f_likes + 0,026 * f_likes * (log_pob - media_log_pob)
```

donde `f_likes` = logit(dominancia de likes) y `log_pob` = logaritmo de la poblacion municipal.

**Interpretacion de cada coeficiente:**

- **beta_0 = 0,258:** cuota predicha para el candidato promedio en la ciudad promedio. Consistente con 3,84 candidatos por contienda: 1/3,84 aprox. 26%.
- **beta_1 = 0,111:** por cada unidad adicional en el logit de dominancia, la cuota en log-odds sube 0,111. En terminos practicos: pasar del 25% al 50% de dominancia digital corresponde a un incremento en logit de aprox. 1,1 unidades, lo que se traduce en aprox. 10 pp adicionales de cuota predicha.
- **beta_2 = 0,026:** el moderador. En ciudades grandes (log-pob por encima de la media), el efecto total de la senal es beta_1 + beta_2 x desviacion. Dominar las redes sociales pesa mas electoralmente en ciudades grandes.

**Las 7 variables restantes penalizadas a cero:** su contribucion marginal al MAE fuera de muestra era negativa. ElasticNet las descarto automaticamente.

---

## PASO 11: Aplicacion prospectiva 2026

El modelo entrenado en 31 elecciones de alcaldes se aplico SIN reentrenamiento a la segunda vuelta presidencial del 21 de junio de 2026.

**Correccion metodologica necesaria:** el modelo fue entrenado con intercepto aprox. 0,258 (base de 26%, coherente con 3,84 candidatos). Una segunda vuelta tiene exactamente 2 candidatos y base del 50%. Se elimino el intercepto y se re-centro sobre el 50%:

```
p_hat_c_segunda_vuelta = 0,50 + (beta_1 * f_likes + beta_2 * f_likes * (log_pob - media))
```

**Datos 2026:** 444 publicaciones totales, FB + TW + TikTok, ventana de 14 dias.

| Candidato | Likes | Dominancia |
|---|---|---|
| Cepeda Castro | 17.087.679 | 77,6% |
| De la Espriella | 4.926.361 | 22,4% |

**Pronostico:** Cepeda 60,5%, De la Espriella 39,5%.

**Resultado real:** De la Espriella 50,48%, Cepeda 49,52%. Margen: 0,96 pp.

**MAE 2026:** |60,5% - 49,52%| = **10,98 pp**, que supera el MAE historico en 1,42 pp.

La senal de Cepeda era real (3,5 veces mas likes). Pero el margen fue menor al propio error del modelo. Ninguna herramienta basada en engagement puede resolver contiendas de empate tecnico.

---

## Cronologia resumida

```
EXTRACCION oct. 2023 (Playwright + Apify)
         |
RESTAURACION WEIBULL (aplicar parametros Costa Rica)
         |
VALIDACION DE SENAL (Mann-Whitney p=0,0481 + permutacion p<0,0001 + Spearman)
         |
NORMALIZACION (3 familias de variables, transformacion logit)
         |
REDUCCION VIF (22+ variables, VIFs hasta 351 -> 9 variables conceptualmente distintas)
         |
AUTOML (9 especificaciones x 5 familias de modelos, GLM fraccional gana)
         |
ELASTICNET ANIDADO (CV interno elige alpha=0,0475 y l1=0,10, CV externo mide MAE)
         |
LOCO-CV (31 pliegues, MAE = 9,56 pp, R2oos = 0,518)
         |
APLICACION 2026 (sin reentrenamiento, MAE = 10,98 pp)
```

---

## Preguntas frecuentes de jurado y respuestas

**"Las correlaciones Spearman son composicionales, por que las reporta?"**
Hay que distinguir dos preguntas y se tiene la respuesta numerica exacta para ambas:

(1) La senal digital, existe o es artefacto? El test de permutacion intra-contienda (barajando etiquetas ganador/perdedor dentro de cada ciudad) da p menor que 0,0001. La senal existe.

(2) Cuanto del rho = 0,70 es composicional y cuanto es senal real? Se cuantifica con una segunda permutacion: reasignar los likes aleatoriamente entre candidatos DENTRO de cada ciudad (preservando el total de likes por ciudad, pero eliminando la relacion likes-votos). El rho promedio bajo esa hipotesis nula composicional es 0,261 (rango de las 10.000 iteraciones: -0,020 a 0,567).

Descomposicion exacta (datos reales, 10.000 iteraciones, semilla = 42):

| Componente | rho | Porcentaje |
|---|---|---|
| Composicional (inflacion mecanica) | 0,261 | 39% |
| Senal predictiva real | 0,409 | 61% |
| rho observado total | 0,670 | 100% |

El rho observado (0,670) supera el percentil 95 de la distribucion nula (0,397) y el p-valor empirico es menor que 0,0001: ninguna de las 10.000 permutaciones alcanzo el rho real.

Conclusion para la defensa: el 39% del rho se debe a composicionalidad mecanica (el hecho de que ambas variables comparten denominador). El 61% restante (rho aprox. 0,41) es senal predictiva genuina entre likes y votos. La advertencia composicional reduce el rho efectivo de 0,70 a 0,41, que sigue siendo altamente significativo. La funcion de esa correlacion en la tesis es exclusivamente ilustrativa (dominancia es mas informativa que volumen bruto); la validez predictiva real la da el LOCO-CV con MAE = 9,56 pp.

**"Por que el Top-1 baja de 71% a 64,5% en el modelo?"**
Minimizar MAE de magnitud y maximizar exactitud de clasificacion ordinal son objetivos distintos. El modelo sacrifica algo de exactitud de ranking a cambio de estimaciones de magnitud mas calibradas. El Top-1 es metrica derivada de la regresion; no hay un clasificador entrenado.

**"Como controlo el sobreajuste?"**
Dos niveles: (1) CV interno elige hiperparametros antes de ver el pliegue externo. (2) LOCO-CV externo mide MAE sobre la ciudad excluida completa. La aplicacion a 2026 es un tercer nivel: fuera de muestra en formato de eleccion distinto.

**"El test de permutacion da p<0,0001 pero Mann-Whitney da p=0,0481 - son inconsistentes?"**
No. Son pruebas de hipotesis distintas. Mann-Whitney compara distribuciones mancomunadas asumiendo independencia. El test de permutacion controla la estructura de anidamiento. Que el test de permutacion sea mas significativo indica que el resultado es robusto incluso al controlar el agrupamiento. Ambos apuntan en la misma direccion: la senal es real.

**"Los VIFs son enormes - por que no elimino variables antes de modelar?"**
Eliminar variables manualmente por VIF es una forma de seleccion por conveniencia, no por desempeno predictivo. En cambio, ElasticNet tolera la colinealidad y hace la poda automaticamente por MAE fuera de muestra. Las variables que "sobran" (por colinealidad) son penalizadas a cero sin necesidad de decision manual.

**"Por que solo el MAE como criterio de seleccion en el AutoML? No considera R2, RMSE, AIC?"**
Porque es el unico criterio que mide directamente lo que el modelo tiene que hacer: cuantos puntos porcentuales te equivocas al estimar la cuota de voto. Es directamente interpretable por cualquier audiencia sin saber estadistica. Los demas indicadores se reportan como diagnostico complementario pero no se usan para seleccionar:

- RMSE penaliza errores grandes al cuadrado, sensible a outliers. Con n=120, un candidato muy mal predicho dominaria el indicador.
- R2oos depende de la varianza de la muestra, no solo del error. Dos modelos con el mismo MAE pueden tener R2 distintos segun la varianza del subconjunto.
- Top-1 (clasificacion) fue explicitamente descartado porque minimizar MAE de magnitud y maximizar exactitud ordinal son objetivos distintos. La tabla de especificaciones lo demostro: el modelo final (64,5% Top-1) es peor clasificador que el baseline (71%) pero mucho mejor estimador de magnitud.
- AIC y BIC miden la bondad de ajuste en entrenamiento penalizada por complejidad, no el error fuera de muestra real.

El notebook lo enuncia explicitamente en la celda 0 del proceso AutoML: "Metrica unica: MAE de la cuota de voto (puntos porcentuales), siempre al lado del baseline de proporcionalidad."

**"Por que esos modelos especificos en el AutoML y no otros?"**
No fue un AutoML de libreria que prueba 200 modelos automaticamente. Fue un proceso acotado con las familias mas plausibles para el problema:

- GLM fraccional: unico modelo teoricamente correcto para variable dependiente en (0,1); garantiza predicciones en ese rango por construccion (Papke y Wooldridge, 1996).
- Gradient boosting: mejor modelo de arboles para datos tabulares segun literatura reciente; captura no-linealidades sin supuestos distribucionales.
- Redes neuronales: aproximador universal; se incluyo para descartar formalmente.
- Random forests: ensemble clasico con buena resistencia a sobreajuste.
- SVM: kernel trick; captura relaciones no lineales en espacios de alta dimension.

Se excluyeron deliberadamente metodos bayesianos (requieren prior sobre la distribucion del voto, no disponible), modelos de series de tiempo (el problema es transversal, no longitudinal) y deep learning (no justificado con n=120).

**"El MAE de 9,56 pp salio de la ciudad excluida en cada pliegue del LOCO-CV?"**
Si, completamente. En cada uno de los 31 pliegues, el modelo predice candidatos de una ciudad que nunca vio durante el entrenamiento. El MAE final es el promedio de esos 31 errores individuales sobre ciudades nunca vistas. No hay ningun candidato que haya sido predicho por un modelo que lo conocia de antemano. Por eso se llama estimacion "honesta" fuera de muestra.

**"LOCO-CV es una metodologia inventada para esta tesis o existe en la literatura?"**
No es una invencion. Es una adaptacion directa del metodo estandar de machine learning "Leave-One-Group-Out Cross-Validation (LOGO-CV)", que aparece en scikit-learn como LeaveOneGroupOut (exactamente la clase que usa el codigo del notebook). El metodo tiene aplicaciones establecidas en:

- Medicina y epidemiologia: se llama "Leave-One-Site-Out" cuando los datos vienen de multiples hospitales. Es el estandar de oro para estimar transferibilidad a nuevos centros.
- Econometria espacial: datos agrupados por cluster (candidatos dentro de ciudades son exactamente un caso de cluster).
- Pronostico de series de tiempo multi-mercado: se excluye un mercado completo en cada pliegue para estimar transferibilidad a mercados nuevos.

La adaptacion terminologica de la tesis fue llamarla "Leave-One-Contest-Out" para hacer explicito que el "grupo" es una contienda electoral completa, no una observacion. El concepto subyacente es identico al estandar de scikit-learn.

Por que es necesario en vez de K-Fold estandar: las cuotas de likes y de votos de todos los candidatos de una ciudad suman 1 por definicion (son composicionales). Si partes esos candidatos aleatoriamente entre entrenamiento y prueba, el modelo ve en entrenamiento que el candidato A de Medellin tiene 40% de likes, y cuando predice al candidato B de Medellin (en prueba) ya sabe implicitamente que B no puede tener mas del 60%. Eso es fuga de informacion y produce evaluaciones de desempeno artificialmente optimistas.

---

## Preguntas del guion (Prioridad 1 y 2)

### PRIORIDAD 1 — Casi seguro van a aparecer

**"Encontramos tres juegos de coeficientes distintos para el mismo modelo"**
Los tres corresponden a tres especificaciones distintas:
1. beta_1 = 0,111 y beta_2 = 0,026: modelo de 2 predictores, los definitivos, con LOCO-CV externo.
2. beta_mod = 0,557: ElasticNet sobre el pool completo de 9 variables.
3. beta aprox. 0,423: regresion fraccional simple de la Seccion 5.6.a, sin ElasticNet.
La tesis tiene una tabla unificada de reconciliacion que los compara directamente.

**"Cual modelo se aplico en 2026 y de que modelo es el MAE = 9,56?"**
El modelo de 2 predictores, ElasticNetCV, StandardScaler, sobre las 31 contiendas colombianas. El MAE de 9,56 pp es de ese modelo bajo LOCO-CV. El 9,57 pp pertenece al pool completo de 9 variables. Son especificaciones distintas con resultados practicamente identicos.

**"El +/- MAE no es un intervalo de prediccion formal"**
Correcto. El MAE es exactitud promedio, no dispersion. Esa construccion fue corregida en la tesis. Lo que se dice ahora: el resultado real de 49,52% supera el limite de referencia heuristica en 1,42 pp. Un intervalo formal requeriria supuestos distribucionales adicionales.

**"El filtro de 10.000 votos crea sesgo de seleccion sobre la variable dependiente"**
Es una limitacion real, reconocida explicitamente. Las metricas reportadas reflejan el subconjunto mas predecible. Esta limitacion es inherente al diseno en ausencia de un criterio de exclusion que no dependa de los resultados.

**"Que hicieron con los candidatos sin publicaciones donde el logit no esta definido?"**
Se imputo dominancia minima epsilon = 10^-3 (0,1%), produciendo logit(0,001) aprox. -6,91. Analisis de sensibilidad: con epsilon = 1% el valor seria -4,60, una diferencia de 2,31 unidades-logit que multiplicada por beta = 0,111 desplazaria la prediccion aprox. 26 pp. Los candidatos afectados (aprox. 9 de 120) son los menos votados y ElasticNet los penaliza fuertemente.

---

### PRIORIDAD 2 — Pueden aparecer como seguimiento

**"Los parametros Weibull estan mal interpretados"**
En F(t) = 1 - e^(-k(t+t0)^alpha):
- k es una tasa (no escala clasica).
- alpha controla la geometria: alpha menor que 1 desacelera; alpha mayor que 1 la tasa crece. Twitter/X con alpha = 1,14 refleja acumulacion acelerada (mecanismo de retweet).
- t0 es un adelanto de origen: hace que F(0) sea mayor que 0, modelando interacciones previas al primer dia de observacion.

**"Mann-Whitney asume independencia; el Spearman de 0,70 es composicional"**
p = 0,0481 es del engagement por publicacion. La estructura de anidamiento se valida con test de permutacion intra-contienda (p menor que 0,0001). El Spearman es evidencia exploratoria; la validez predictiva real se establece por LOCO-CV. El rho aprox. 0,45 del volumen absoluto confirma que la dominancia es mas informativa. La composicionalidad esta cuantificada: rho_mec = 0,261 (39%), senal real rho_real aprox. 0,41 (61%).

**"Que mide realmente el modelo: intencion de voto o cuota electoral?"**
ELA-NOM aproxima la cuota electoral observada, no la intencion de voto latente. El proxy digital puede capturar apoyo genuino, visibilidad, polarizacion y pauta paga simultaneamente. El unico claim predictivo: cuota de likes predice cuota de votos con MAE = 9,56 pp fuera de muestra.

**"El OE4 anuncia clasificacion Y regresion, pero solo hay regresion"**
El Top-1 del 64,5% es una metrica derivada de la regresion, no un clasificador entrenado independientemente. El OE4 fue reformulado en la tesis. Un logit condicional de McFadden queda como trabajo futuro.

---

### OTRAS PROBABLES

**"Por que excluir Instagram de Colombia?"** Meta cerro su API para investigadores independientes en 2023. Restriccion externa del ecosistema, no una decision metodologica.

**"El error en 2026 fue de 10,98 pp. No invalida el modelo?"** El MAE medio es 9,56 pp. El margen real fue de 0,96 pp, inferior al propio error del modelo. Ninguna herramienta basada en engagement puede resolver un empate tecnico. El uso correcto de ELA-NOM es detectar tendencias y ventajas claras superiores a 20 pp.

**"El R2 del Weibull es muy bajo?"** El R2 promedio de 0,449 incluye el 66,8% de varianza que es ruido intra-publicacion irreducible. El modelo captura la forma global de la curva, que es lo que necesita para la reconstruccion historica.

**"Por que no normalizar por seguidores?"** El numero de seguidores es inestable entre plataformas, altamente colineal con el volumen de publicaciones y no disponible historicamente en todas las plataformas. VIF elevado lo descarto automaticamente del pool.

**"Por que la dominancia relativa y no el volumen absoluto?"** Clasificador naive: dominancia 71% vs volumen bruto 57,6%. Spearman: rho = 0,70 vs rho aprox. 0,45. La dominancia elimina el efecto del tamano de la contienda y mide la senal competitiva directamente.

**"Cuanto cuesta replicar esto?"** Entre 20 y 30 dolares en creditos de Apify. Procesamiento corre en cualquier computador con Python.
