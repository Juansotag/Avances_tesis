# Correcciones detalladas — Tesis ELA-NOM (Juan Sotelo Aguilar)

**Propósito de este documento**: contiene, punto por punto, las observaciones textuales completas de los jurados Andrés Cruz y Adrián Santana, junto con la ubicación exacta en el documento (capítulo, sección, página impresa de la tesis) y, cuando aplica, el fragmento textual exacto del documento que motivó el comentario. Está pensado para que otro agente/editor pueda ir sección por sección corrigiendo sin tener que releer los PDFs de revisión.

**Documento fuente de la tesis**: `Diseño_e_implementación_del_modelo_ELANOM__Juan_SoteloAguilar.pdf` (el mismo que se revisó).

**Convención de referencia de ubicación**: se da el número de página impresa de la tesis (el que aparece al pie de cada página, no el número de página del archivo PDF), junto con el capítulo y sección correspondiente según el índice general del documento.

---

## TABLERO DE ESTADO — Última actualización: 2026-08-09 (auditoría final de archivos)

### ✅ Corregidas (25/25) — COMPLETO

| # | Descripción resumida | Archivo(s) editado(s) | Cómo se resolvió |
|---|---|---|---|
| 1.1a | Citas sin paréntesis → `\parencite` | `introduccion.tex` | Búsqueda global y reemplazo de `\cite{` → `\parencite{` |
| 1.1b | Separadores decimales: punto → coma | `metodologia.tex`, `resultados.tex` | Reemplazo sistemático de `{numero}.{decimales}` → `{numero}{,}{decimales}`. Residuos en L102 y L193 corregidos. |
| 1.1c | Índices de figuras, cuadros y siglas | `main.tex` | Agregados con `\listoffigures`, `\listoftables` y entorno `\printglossary` |
| 1.2 | Comparación Polymarket/Kalshi (facturación ≠ volumen transado) | `introduccion.tex` | Reescritura del párrafo aclarando que son magnitudes distintas y que la comparación es solo ilustrativa |
| 1.3 | Base de cálculo porcentajes DataReportal | `introduccion.tex` | Se declaró explícitamente que los porcentajes por plataforma son sobre usuarios de redes sociales (base ≠ población total) |
| 1.4/1.5 | Codominio de f: `[0,1]^C` → `[0,1]` (escalar, no vectorial) | `introduccion.tex` | Corregida ecuación 1.2 para que coincida con ecuación 3.1 del Cap. 3 |
| 1.6 | Interpretación parámetros Weibull (k, α, t₀) | `metodologia.tex`, `marco-conceptual.tex` | (1) k redescrito como tasa, no escala; (2) α: se aclaró que solo captura deceleración si α<1, y que Twitter/X con α=1,1422 muestra tasa creciente; (3) "decaimiento exponencial" eliminado; (4) t₀: corregido a "adelanto" del origen (no retardo). Aplicado en Cap. 5 (metodologia.tex) y Cap. 3 (marco-conceptual.tex L67). |
| 1.7 | Variable latente vs. escalar fijo | `metodologia.tex` | Sección 5.1.b reescrita para distinguir i_e(t) (variable teórica dinámica) de i(e,cj) (valor operacionalizado en t=tf) |
| 1.8 | Ecuación suma votos: Σv(e,cj)=1 → Σv(e,cj)=ve | `metodologia.tex` | Corregida la ecuación; agregada ecuación separada Σi(e,cj)=1 para las cuotas |
| 1.9 | MAE=RMSE en Tabla 6.1 (n=1) + nota metodológica | `resultados.tex`, `metodologia.tex` | Eliminada columna RMSE (redundante con n=1); agregada nota al pie explicando el cálculo sobre un único punto y el cociente heurístico MAE_test/MAE_encuestas ≈ 1,2. Se moderó "superó considerablemente" → "superó" |
| 1.10 | Instagram: excepción al 20% es Día 1, no Día 3 | `metodologia.tex` | Reescrita la frase para decir que a partir del Día 3 **las cuatro** plataformas están bajo el 20%; la excepción es Día 1 (Instagram 20,72%). Agregada justificación del umbral como criterio pragmático. |
| 1.11 | Repositorio público y entorno reproducible | `refs.bib`, `impacto-esperado.tex`, `metodologia.tex` | Generado `requirements_tesis.txt`, agregada cita `sotelo2026elanom` a BibTeX con versiones explícitas y moderada la frase de "reproducibilidad absoluta" → "documentada y reproducible". |
| 1.16/2.2 | Mann-Whitney y Spearman composicional | `resultados.tex` | Redacción de la Sección 6.3.a actualizada: (1) aclara que Mann-Whitney mide mediana de engagement y reporta test de permutación intra-contienda; (2) incluye correlación del volumen absoluto (ρ ≈ 0,45); (3) añade IC 95% de Wilson [53,4%-83,9%] para el 71% de aciertos; (4) aclara naturaleza composicional y delega validez predictiva a LOCO-CV. |
| 1.18 | Tono retórico en secciones 6.2, 6.4 y 8.1 | `resultados.tex`, `conclusiones.tex` | (1) "formidables" → "robustos"; (2) "soluciona drásticamente" → "resuelve" + caveat de generalización; (3) "asimetría temporal del SOMEN-DC" → "no transferibilidad del SOMEN-DC" (corrección conceptual); (4) "total escalabilidad / analfabetismo algorítmico" → lenguaje factual; (5) "como quedó demostrado en la segunda vuelta de 2026" → "como se exploró prospectivamente…, donde el error fue de 10,98 pp y no se acertó el candidato ganador" |
| 1.19 | Pregunta legal: Ley 2494 de 2025 | `impacto-esperado.tex` | Agregado párrafo señalando la ambigüedad regulatoria: ELA-NOM podría no encuadrar como "encuesta electoral" por no usar sondeo directo, pero el resultado es funcionalmente análogo; se recomienda asesoría jurídica antes de despliegue público |
| 1.20 | OE4 (regresión vs clasificación) y OE2 (tabla de crecimiento) | `objetivos.tex`, `introduccion.tex`, `metodologia.tex` | (1) OE4 ajustado para explicitar regresión fraccional primaria con Top-1 derivado; (2) Añadida Tabla 5.2 comparando empíricamente Exponencial (R²=0,182), Logístico (R²=0,245) y Weibull (R²=0,449). |
| P3/P4 | Preguntas derivadas 3 (tracción tardía) y 4 (curva de aprendizaje) | `resultados.tex` | Añadida Sección 6.3.5 con: (a) Tabla de curva de aprendizaje (5–30 contiendas, 50 repeticiones, seed=42): MAE baja de 12,82pp a 12,05pp — reducción de 0,77pp en total, curva prácticamente plana; conclusión honesta: el piso de error (~12pp) es estructural, no por falta de datos; (b) Comparación Spearman dominancia 14 días (ρ=0,7036) vs tracción tardía (ρ=0,6655): Δρ=0,038, diferencia pequeña; la ventana acumulada ya captura la mayor parte de la señal; (c) Figura `col_learning_curve.png` incluida. |
| 2.1 | Proxy digital: ELA-NOM no mide intención de voto stricto sensu | `marco-conceptual.tex` | Sección 3.3 expandida: se declaró que el modelo aproxima la **cuota electoral** (no la intención de voto) y se nombraron 4 fuentes alternativas de varianza: visibilidad mediática, polarización/rechazo, pauta paga, militancia organizada |
| 2.3 | Niveles de validación fuera de muestra y ElasticNet | `metodologia.tex` | Sección 5.6.b actualizada: (1) ecuación explícita de ElasticNet y función de pérdida (L1/L2); (2) estructura explícita de dos niveles out-of-sample: Nivel 1 (LOCO-CV por contienda) y Nivel 2 (prospectiva 2026 por formato). |
| 2.5 | Claridad narrativa sobre rol de cada etapa empírica | `metodologia.tex` | "Diseño general del proceso" reescrito como lista explícita con Etapa 1/2/3 y Validación, cada una con su rol, problema técnico resuelto y preguntas (P1-P4) que responde |
| 1.17/2.4 | MAE usado como intervalo de predicción | `resultados.tex`, `metodologia.tex`, `resumen.tex` | **En `resultados.tex`**: reemplazado "intervalo de incertidumbre (rango plausible 51%--70%)" por lenguaje de referencia heurística; se corrige que el error de 10,98pp **superó** el MAE (no "cae dentro"). **En `metodologia.tex` L359** (corregido en auditoría 2026-08-09): reemplazado "el MAE sitúa el intervalo de pronóstico plausible entre 50,9% y 70,1%" por texto explícito que aclara que el ±MAE **no es un intervalo probabilístico ni tiene cobertura declarada**, que sirve solo como referencia de magnitud, y que el resultado real (49,52%) **supera** ese límite inferior en 1,42 pp. **En `resumen.tex`**: el error "supera en 1,42 pp el MAE medio" — formulado correctamente. |
| 1.12 | Sesgo de selección: filtro >10.000 votos + exclusión de Bogotá | `metodologia.tex` | (1) **Filtro >10.000 votos** (`metodologia.tex` L262, nota al pie 1): reconoce explícitamente el **sesgo de selección sobre la variable dependiente** — umbral arbitrario que excluye candidatos con peor desempeño electoral, sesgando MAE/R² hacia el subconjunto más predecible; declara que esta limitación es inherente al diseño en ausencia de criterio independiente de resultados. (2) **Bogotá / Gustavo Bolívar** (`metodologia.tex` L262, nota al pie 2): documenta la violación del **supuesto de localidad geográfica** — GB es libretista/escritor con audiencia panlatinamericana; mayoría de sus interacciones no proviene de electores bogotanos; incluirlo habría asignado señal masiva a cuota moderada (3° lugar). Se advierte que el modelo no está calibrado para candidatos con audiencias supranacionales. |
| 1.13 | Imputación de dominancia=0 (logit indefinido) | `metodologia.tex` | Nota al pie a la ecuación del logit de dominancia (`metodologia.tex` L283) documentando: (a) ε = 10⁻³ (0,1%) usado en la función `to_logit` de `generar_figuras_colombia.py`; (b) logit(0,001) ≈ −6,91 para los ~9 candidatos sin publicaciones activas; (c) análisis de sensibilidad: con ε=1% el logit sería −4,60 — diferencia de 2,31 logit-unidades que multiplicada por β≈0,111 desplazaría la predicción en ~26 pp. Confirma que declarar ε es esencial para replicabilidad. |
| 1.14 | Tres juegos distintos de coeficientes ElasticNet | `resultados.tex` | (1) **β_mod=0,557** documentado en nota al pie (`resultados.tex` L171): corresponde al coef. medio del moderador cuando ElasticNet opera sobre el pool completo de 9 variables (no a la especificación final de 2 variables). (2) **Caption de Figura 6.4** (`resultados.tex` L176) corregido: aclara que los valores mostrados (β≈0,42) son del modelo de regresión fraccional simple (Sección 5.6.a), **no** del ElasticNet final. (3) **β₁=0,111 y β₂=0,026** del texto son correctos para el modelo de 2 variables con StandardScaler (alpha=0,0475, L1=0,10, intercepto=0,258). Los tres juegos quedan reconciliados sin ambigüedad. |
| 1.15 | Modelo aplicado en 2026 + MAE de referencia incorrecto | `resultados.tex`, `resumen.tex` | (1) **Modelo aplicado**: especificación de 2 predictores (`f_likes_dom` + `mod_likes_pob`) entrenado con ElasticNetCV(random_state=42) sobre 31 contiendas, con StandardScaler — documentado en `resultados.tex` L189. (2) **Fórmula del 60,5%** documentada en `resultados.tex` L216: señal=0,2294 → 0,50+0,2294=0,729 → 0,729/(0,729+0,477)=60,5%. (3) **MAE verificado en auditoría**: el MAE de la especificación de 2 predictores (LOCO-CV) es **9,56 pp** en todos los archivos — el valor 10,37 pp mencionado en el tablero anterior **no existe en ningún archivo** (búsqueda → 0 resultados); 9,57 pp es el ElasticNet sobre el pool completo. (4) **"9,43 pp" eliminado**: búsqueda global → 0 resultados. ✅ Los archivos son internamente consistentes; la descripción del tablero previo tenía un error en el MAE reportado.



---

### ⚠️ Pendientes (0/25)

#### 🔴 Prioridad 1 — BLOQUEANTES
*Sin pendientes.*

#### 🟡 Prioridad 2 — Importantes

---



## PARTE 1 — Observaciones de Andrés Cruz

> Nota técnica: estos comentarios estaban como anotaciones/highlights insertados directamente en el PDF de la tesis (no como texto corrido), por lo que se pudo extraer tanto el comentario textual completo como el fragmento exacto del documento que fue resaltado.

### 1.1 — Notas generales (página 1, notas adhesivas sin anclaje a un pasaje específico)

**Comentario textual completo:**
> "Unificar el estilo de citación en toda la extensión del trabajo y verificar la construcción de cada referencia (hay referencias sin paréntesis).
>
> Fijar la coma como separador decimal y el punto como separador de millar en todo el documento, incluidos tablas y figuras, y regenerar las cifras afectadas.
>
> Incorporar índice de figuras, índice de cuadros y un listado de siglas en los preliminares."

**Acción requerida:**
1. Revisar todas las citas del documento (formato APA o el que corresponda) y verificar que todas usen paréntesis de forma consistente.
2. Buscar y reemplazar de forma sistemática: usar coma decimal (`9,43` en vez de `9.43`) y punto para miles (`120.000` en vez de `120,000`) en **todo** el documento — texto, tablas y figuras (esto implica regenerar las figuras hechas con matplotlib/seaborn si tienen números en notación inglesa).
3. Agregar al frente del documento (preliminares, después del índice general): índice de figuras, índice de cuadros, y listado de siglas (SOMEN-DC, ELA-NOM, MAE, MAPE, RMSE, VIF, LOCO-CV, GLM, GRNN, MLP-BP, PCA, CNE, ACEI, ESOMAR, etc.).

Segunda nota adhesiva en la misma página (sin contenido legible, marcada como "None definida por andre" — posiblemente una anotación vacía o corrupta; no requiere acción, pero vale confirmar con el jurado si quedó algo pendiente ahí).

---

### 1.2 — Página impresa 1 / PDF p.6 — Capítulo 1, Sección 1.1 "Motivación del problema"

**Fragmento exacto del documento resaltado:**
> "Este crecimiento contrasta con el de los mercados alternativos de pronóstico: plataformas como Polymarket y Kalshi registraron en conjunto cerca de 60.000 millones de dólares en volumen de operaciones..."

**Comentario textual completo:**
> "El contraste entre los 153.000 millones de dólares de la industria y los 60.000 millones de Polymarket y Kalshi no es comparable: lo primero es facturación anual y lo segundo es volumen transado, magnitudes de naturaleza distinta."

**Acción requerida:** Reformular el párrafo de apertura de 1.1 para no comparar directamente ambas cifras como si fueran la misma magnitud. Alternativas: (a) buscar una cifra de facturación/ingresos de las plataformas de mercados de predicción para comparar peras con peras, o (b) mantener ambas cifras pero aclarar explícitamente que son magnitudes distintas (facturación vs. volumen transado) y que la comparación es solo ilustrativa del crecimiento relativo de interés en información predictiva, no una comparación de tamaño de mercado.

---

### 1.3 — Página impresa 5 / PDF p.10 — Capítulo 1, Sección 1.3 "Hipótesis de trabajo"

**Fragmento exacto del documento resaltado:**
> "...este argumento pierde fuerza en la medida en que la cobertura digital se aproxima a la universalidad. Según DataReportal (2025), el 70,4 % de la población colombiana usa redes sociales al cierre de 2025, cifra que creció en 1,6 millones de personas solo en 2024, con Facebook, TikTok, YouTube, Instagram y LinkedIn alcanzando al 89,3 %, 93,0 %, 74,4 %, 52,3 % y 44,4 % de los adultos colombianos, respectivamente."

**Comentario textual completo:**
> "Estas cifras no cuadran entre sí. Si apenas el 70,4 % de la población usa redes, ninguna plataforma puede alcanzar al 89,3 % ni al 93,0 % de los adultos. Lo más probable es que los porcentajes por plataforma estén calculados sobre la base de usuarios de redes, no sobre el total de adultos, o que correspondan a audiencia publicitaria, que es otra métrica. Hay que revisar la fuente y declarar la base de cada cifra, porque el 12,0 % de X/Twitter viene del mismo cálculo y de él depende un juicio importante del capítulo."

**Acción requerida:**
1. Volver a la fuente original de DataReportal / Digital 2026: Colombia y verificar la base de cálculo real de cada porcentaje (¿es sobre población total, sobre población adulta, sobre usuarios de internet, o es "audiencia potencial de anuncios" — una métrica publicitaria que normalmente excede el 100% de superposición entre plataformas?).
2. Reescribir el párrafo declarando explícitamente la base de cada cifra (ej. "X % de la población adulta con acceso a internet" vs. "X % de audiencia potencial publicitaria").
3. Esto es especialmente importante porque el argumento de que "X/Twitter solo alcanza al 12,0% de los adultos, comprometiendo estructuralmente cualquier modelo que dependa exclusivamente de esa fuente" depende de esta misma base de cálculo — si cambia la base, cambia la fuerza del argumento.

---

### 1.4 — Página impresa 5 / PDF p.10 — Capítulo 1, Sección 1.3 (ecuación 1.2, formalización del problema)

**Fragmento exacto del documento resaltado:**
> "La hipótesis central de este trabajo postula que existe una función: f : Rᵈ → [0, 1]ᶜ" (ecuación 1.2)

**Comentario textual completo:**
> "Hay una inconsistencia en el dominio y el codominio. Si f va de R^d a [0,1]^C, entonces su argumento debería ser el conjunto de vectores de toda la contienda y no el vector x_i de un solo candidato; tal como está escrito, f(x_i) devolvería un vector de dimensión C para un único candidato."

**Acción requerida (CRÍTICO — ver también 1.5 abajo, es la misma inconsistencia repetida en el Cap. 3):**
Definir con precisión y de forma única en todo el documento si:
- **Opción A**: f recibe el vector de características de un solo candidato y devuelve un escalar (su cuota de voto individual): f: R^d → [0,1]. Esta es la definición usada en la práctica en el resto de la metodología (regresión fraccional, ElasticNet).
- **Opción B**: f recibe la matriz/conjunto de vectores de toda la contienda y devuelve el vector completo de cuotas de todos los candidatos: f: R^(d×C) → [0,1]^C (con la restricción de que sume 1).

Dado que el resto de la tesis (capítulo 5 y 6) efectivamente modela candidato por candidato con un GLM aplicado a cada fila del dataset, la definición correcta y consistente con lo que realmente se implementó es la **Opción A** (codominio escalar). Hay que corregir la ecuación 1.2 en el Capítulo 1 para que coincida con la ecuación 3.1 del Capítulo 3 (ver punto 1.5), y explicar aparte cómo se logra la restricción de suma-1 (probablemente vía normalización posterior, no como parte de la definición de f).

---

### 1.5 — Página impresa 9 / PDF p.14 — Capítulo 3, Sección 3.2 "Modelos elección-agnósticos: definición y ventajas" (ecuación 3.1)

**Fragmento exacto del documento resaltado:**
> "Formalmente, sea E = {e₁, e₂, . . . , eM} un conjunto de M elecciones históricas diferentes (por ejemplo, alcaldías de distintas ciudades). El objetivo es aprender una función predictiva: f : Rᵈ → [0, 1]" (ecuación 3.1)

**Comentario textual completo:**
> "La ecuación (3.1), define f de R^d a [0,1], es decir con codominio escalar, lo cual contradice la definición del capítulo 1. Una de las dos debe corregirse."

**Acción requerida:** Ver punto 1.4. Esta es la definición que sí coincide con lo implementado — corregir la ecuación 1.2 del Capítulo 1 para que sea consistente con esta.

---

### 1.6 — Página impresa 10 / PDF p.15 — Capítulo 3, Sección 3.4 "El problema del histórico de interacciones" (ecuación 3.2, parámetros de la Weibull)

**Fragmento exacto del documento resaltado:**
> "...es el parámetro de escala que determina la velocidad general de acumulación; α es el parámetro de forma que captura la rápida deceleración típica del consumo de contenido en redes (decaimiento exponencial); y t₀ modela la asimetría temporal inicial, capturando la explosión masiva de interacciones que ocurre en las primeras horas antes de que t se convierta en 1 día."

**Comentario textual completo:**
> "La interpretación de los parámetros no coincide con lo que hace la función. Primero, en la parametrización que se escribe, k no es un parámetro de escala sino una tasa.
> Segundo, α solo captura deceleración cuando α < 1. En la Tabla 5.1 Twitter/X queda calibrado con α = 1,1422, es decir con riesgo creciente, es pertinente aclarar. Por otro lado, "decaimiento exponencial" corresponde al caso α = 1, que es el modelo que se descarta, de modo que la expresión resulta contraproducente aquí.
> Tercero, y lo más importante, t0 > 0 no introduce un retardo sino lo contrario."

**Acción requerida (afecta también la Sección 5.4.d donde se repite la misma explicación):**
1. Corregir la descripción de k: en la parametrización Weibull usada (F(t) = 1 - e^(-k(t+t0)^α)), k tiene unidades de tasa (no de escala en el sentido clásico de la distribución Weibull estándar, donde la escala λ aparece como t/λ). Aclarar esto o reparametrizar si se quiere mantener la interpretación de "escala".
2. Corregir la afirmación de que α "captura la rápida deceleración" — esto solo es cierto si α < 1. Dado que Twitter/X está calibrado con α = 1,1422 > 1 (Tabla 5.1), técnicamente muestra tasa de riesgo creciente en esa parametrización, no deceleración. Hay que revisar qué significa esto físicamente para la curva de Twitter/X y ajustar el texto para que sea coherente con los valores calibrados reales, no con una descripción genérica.
3. Eliminar o corregir la frase "decaimiento exponencial" en relación a α: ese término corresponde específicamente al caso α = 1 (que es el modelo exponencial simple, el que el documento mismo descarta en 5.4.d). Usar una descripción distinta para lo que hace α en general (forma cóncava/convexa de la curva de crecimiento acumulado).
4. Corregir la interpretación de t0: revisar matemáticamente qué hace t0 > 0 en F(t;k,α,t0) = 1-e^(-k(t+t0)^α) — al desplazar t hacia adelante, t0>0 hace que F(0) > 0, es decir, **acelera** la acumulación inicial (ya hay una fracción acumulada positiva desde t=0), no la retrasa. El texto actual dice lo contrario ("modela la asimetría temporal inicial, capturando la explosión masiva... antes de que t se convierta en 1 día" — esto de hecho es correcto en espíritu pero mal explicado como "retardo"; conviene aclarar explícitamente que es un adelanto/aceleración de la curva, no un retardo).

---

### 1.7 — Página impresa 11 / PDF p.16 — Capítulo 5, Sección 5.1.b "Definición de la intención de voto y los resultados" (título de sección resaltado como ancla del comentario)

**Comentario textual completo:**
> "El apartado define la intención de voto como variable latente que evoluciona en t y a renglón seguido la operacionaliza como la cuota de voto del día de la elección, que es un escalar fijo. ¿Son dos objetos distintos?"

**Acción requerida:** Revisar el texto completo de 5.1.b. Actualmente se dice: "Definimos la intención de voto como el número de votantes ve que, en un momento t, escogerían al candidato ce. Esta es una variable subyacente..." (sugiriendo una variable que evoluciona en el tiempo) y luego, un párrafo después, se define i(e,cj) = v(e,cj)/ve como un valor fijo del día de la elección. Se debe aclarar explícitamente que:
- La intención de voto "verdadera" es conceptualmente una variable latente y dinámica (evoluciona con t), pero
- Por restricciones de observabilidad, el estudio **solo observa y modela** su valor en el instante final (t = tf, el día de la elección), que es lo que efectivamente se usa como variable objetivo del entrenamiento.

Sugerencia de redacción: usar notación distinta para el objeto teórico (p. ej. i_e(t)) y el objeto operacionalizado (i(e,cj), fijo), y explicar la relación entre ambos en una frase puente.

---

### 1.8 — Página impresa 12 / PDF p.17 — Capítulo 5, Sección 5.1.b (ecuación de suma de votos)

**Fragmento exacto del documento resaltado:**
> "...donde v(e,cj) es el número de votos del candidato cj para la elección e y ve es el número total de votos para cualquiera de los candidatos de la elección e, es decir Σ(j=1 a |Ce|) v(e,cj) = 1."

**Comentario textual completo:**
> "¿La suma de los votos de todos los candidatos es igual a v_e, o a 1?"

**Acción requerida:** Error de notación claro — la ecuación dice que la suma de v(e,cj) (votos, valores absolutos) es igual a 1, cuando debería decir que es igual a ve (el total de votos). Lo que suma 1 es la suma de las *cuotas* i(e,cj), no de los votos absolutos. Corregir la ecuación a: Σ(j=1 a |Ce|) v(e,cj) = ve, y opcionalmente agregar la ecuación separada Σ(j=1 a |Ce|) i(e,cj) = 1 si se quiere dejar explícita la restricción de las cuotas.

---

### 1.9 — Página impresa 15 / PDF p.20 — Capítulo 5, Sección 5.3.c "Evaluación de modelos" (resultados MLP-BP+PCA, Bolivia)

**Fragmento exacto del documento resaltado:**
> "El modelo con mejor desempeño predictivo resultó ser el ensamble MLP-BP acoplado con PCA, tal como se observa de manera suavizada en la Figura 5.1, alcanzando un Error Absoluto Medio (MAE) de 0.0279 y un Error Porcentual Absoluto Medio (MAPE) aproximado del 5.1 %."

**Comentario textual completo:**
> "La Tabla 6.1 muestra que MAE y RMSE son idénticos en las siete filas, lo cual solo ocurre cuando n = 1. Reportar tres métricas de error para un único punto no agrega información, y hablar de un modelo que "superó considerablemente" a otro con base en una diferencia entre dos números aislados no es sostenible. No hay medida de dispersión, no hay intervalo, no hay forma de distinguir desempeño de incertidumbre."

**Nota adhesiva asociada en la misma página:**
> "Sugiero reportar el MAE sobre toda la ventana de proyección y no únicamente en el día cero, o al menos acompañar la cifra con la desviación de las predicciones en los últimos siete o diez días. Sospecho que el resultado cambia bastante, pero eso es precisamente lo que hay que mostrar."

**Acción requerida (afecta también la Tabla 6.1 y la Sección 6.1 del Capítulo 6, que reporta las mismas métricas para Bolivia):**
1. El MAE, MAPE y RMSE reportados en la Tabla 6.1 (y mencionados en 5.3.c) están calculados sobre un único punto (la predicción del día de la elección para el candidato Paz), lo que hace que MAE = RMSE matemáticamente siempre (con n=1, ambas fórmulas colapsan al mismo valor absoluto). Esto no es un error de cálculo, pero **sí es engañoso presentarlo como si fueran tres métricas informativas distintas**, cuando en realidad es un solo número disfrazado de tres.
2. Recalcular el MAE (y opcionalmente MAPE/RMSE) sobre toda la ventana de proyección (el período de días entre la última encuesta y el día de la elección), no solo sobre el día cero. Esto dará una medida de error con dispersión real (desviación estándar entre días), permitiendo comparar modelos de forma más rigurosa.
3. Ajustar el lenguaje de "superó considerablemente" en 5.3.c y 6.1 para no sobreinterpretar una diferencia entre dos números puntuales sin medida de incertidumbre asociada.

---

### 1.10 — Página impresa 18 / PDF p.23 — Capítulo 5, Sección 5.4.e "Validación: precisión en la estimación del total final" (umbral de 20% e Instagram)

**Fragmento exacto del documento resaltado:**
> "La Figura 5.5 muestra visualmente estos resultados. En el panel izquierdo se observa que el MAPE decae exponencialmente con el día de observación: a partir del Día 3, todos los modelos, excepto Instagram, se ubican por debajo del umbral de referencia del 20 %."

**Comentario textual completo:**
> "La afirmación citada no cuadra con la tabla 6.2. Instagram registra 12,06 % en el Día 3, muy por debajo del umbral de 20 %, de modo que la excepción no aplica en ese día sino en el Día 1, donde marca 20,72 %. Y el umbral del 20 % aparece sin justificación; si va a operar como criterio de aceptación, conviene sustentarlo..."

**Acción requerida:**
1. Verificar la Tabla 6.2 (MAPE mediano por plataforma y día): confirma que Instagram en el Día 3 tiene 12,06% (por debajo del 20%), no por encima. La frase en 5.4.e que dice "a partir del Día 3, todos los modelos, excepto Instagram, se ubican por debajo del 20%" es **fácticamente incorrecta** según la propia Tabla 6.2 — Instagram también está por debajo del 20% en el Día 3. La excepción real ocurre en el **Día 1**, donde Instagram marca 20,72% (por encima del umbral).
2. Corregir la frase en 5.4.e para que sea consistente con los datos de la Tabla 6.2.
3. Agregar una justificación explícita de por qué se usa el 20% como umbral de referencia (¿es un estándar de la literatura? ¿un criterio arbitrario pero razonable? ¿se basa en algún paper citado?). Si no hay justificación clara, considerar reemplazarlo por un criterio más objetivo (p. ej., reportar directamente los percentiles del error sin imponer un umbral binario).

---

### 1.11 — Página impresa 19 / PDF p.24 — Capítulo 5, encabezado de Sección 5.5 "Etapa 3 - Colombia: Construcción del dataset y modelado"

**Comentario textual completo:**
> "Falta el soporte para verificar todo esto. No hay repositorio, ni versiones de librerías, ni semillas, ni anexos, y el archivo de configuración que se menciona en 5.4.f no se aporta. Con eso, ninguna cifra del documento es verificable, y en 7.2 se habla de reproducibilidad absoluta."

**Acción requerida (CRÍTICO):**
1. Publicar o referenciar explícitamente en la tesis el repositorio de código usado para este análisis (nota: el repositorio existente github.com/Juansotag/Avances_tesis puede no estar directamente vinculado en el cuerpo de la tesis — verificar si se menciona y con qué nivel de detalle).
2. Agregar un anexo técnico (o sección de reproducibilidad) que incluya: versiones de las librerías de Python usadas (scikit-learn, statsmodels, scipy, etc.), semillas aleatorias (random_state) usadas en el train/test split y en los modelos estocásticos (MLP-BP, GRNN), y el archivo de configuración de parámetros Weibull mencionado en 5.4.f (los parámetros k, α, t0 por plataforma).
3. Revisar la afirmación de "reproducibilidad absoluta" en la Sección 7.2 (Impacto práctico) — probablemente hay que moderar el lenguaje ahí también, o resolver primero el punto 1 y 2 para que la afirmación sea cierta.

---

### 1.12 — Página impresa 21 / PDF p.26 — Capítulo 5, Sección 5.5 (filtro de 10.000 votos, exclusión de Bogotá/Piedecuesta/Santa Marta)

**Fragmento exacto del documento resaltado:**
> "Para asegurar la validez inferencial, se aplicaron filtros de exclusión: solo ingresaron al dataset actores políticos con más de 10,000 votos confirmados en los escrutinios finales. De las 33 ciudades iniciales se excluyeron dos: la capital Bogotá (por el sesgo de representatividad del perfil influencer de Gustavo Bolívar, cuya masiva tracción supranacional distorsionaba la escala local) y Piedecuesta (porque la candidatura ganadora eliminó intencionalmente sus perfiles digitales ante procesos legales en curso), dejando 31 ciudades competitivas. En casos anómalos como el de Santa Marta, donde la candidatura de mayor votación enfrentó revocatoria legal posterior, el estudio consideró ganador computacional al actor con mayor volumen bruto de votos consignados, para preservar la correlación con la intención ciudadana."

**Comentario textual completo:**
> "Los 10.000 votos son un criterio sobre la variable que se quiere predecir, así que la muestra queda definida por el resultado y eso cambia la lectura de todo lo que viene después, incluidos el MAE de 9,43 y el R² fuera de muestra. Y algo que refuerza el punto: en 6.3.d el modelo se aplica sin ese filtro, porque antes de la elección no hay manera de aplicarlo. Valdría la pena buscar un criterio basado en información previa, o cuando menos mostrar los resultados con y sin filtro para que se vea cuánto pesa.
>
> Lo de Bogotá es más complejo. Se saca el caso porque no se comporta como predice la hipótesis, y encima es la ciudad más grande, la que más peso tendría en la interacción con población que termina siendo el coeficiente dominante. Yo la devolvería y trabajaría a Bolívar como observación influyente, con su diagnóstico y una nota de cuánto se mueven los coeficientes al incluirla. Un atípico bien explicado suma más que uno retirado. Piedecuesta y Santa Marta sí me parecen bien resueltos y bien documentados."

**Acción requerida (CRÍTICO — sesgo de selección, dos problemas independientes):**

*Problema 1 — filtro de 10.000 votos:*
1. Reconocer explícitamente en el texto que el filtro de >10.000 votos es un criterio construido sobre la variable dependiente (los votos obtenidos), lo cual introduce selección post-tratamiento y puede sesgar las métricas de desempeño (MAE=9.43, R²=0.518) hacia arriba (mejor de lo que sería en una muestra sin ese filtro).
2. Idealmente, rehacer el análisis con un criterio alternativo basado en información disponible *antes* de la elección (p. ej., un umbral de interacciones digitales mínimas, o de tiempo de campaña activa, o simplemente incluir a todos los candidatos registrados). Si esto no es viable en el tiempo disponible antes de la sustentación, al menos **reportar las métricas con y sin el filtro** como análisis de sensibilidad, para cuantificar cuánto pesa la decisión.
3. Señalar explícitamente en el texto la inconsistencia metodológica entre el entrenamiento (con filtro de 10.000 votos) y la aplicación prospectiva en 6.3.d (sin filtro, porque antes de la elección no se puede aplicar un criterio basado en resultados) — esto ya lo reconoce el jurado como una limitación real que vale la pena nombrar explícitamente en el texto, no ocultarla.

*Problema 2 — exclusión de Bogotá:*
1. Considerar la recomendación explícita del jurado: **reincorporar a Bogotá** en el análisis, y en su lugar tratar la candidatura de Gustavo Bolívar como una observación influyente/atípica, con un diagnóstico estadístico formal (leverage, distancia de Cook, o similar) y una nota explícita de cuánto cambian los coeficientes del modelo final al incluir vs. excluir esa observación.
2. La razón de peso: Bogotá es la ciudad más grande del dataset, y el coeficiente dominante del modelo final es precisamente la interacción dominancia×población — excluir la observación con mayor población introduce el riesgo de que ese coeficiente esté artificialmente inflado o distorsionado por la ausencia del caso más extremo en la variable de interacción.
3. Piedecuesta y Santa Marta sí quedaron bien resueltos según el jurado — no requieren cambios.

---

### 1.13 — Página impresa 21 / PDF p.26 — Capítulo 5, encabezado de Sección 5.6.a "Modelo de regresión fraccional (cuota de voto)"

**Comentario textual completo:**
> "El predictor central es el logit de la dominancia, y el documento menciona que solo el 92,6 % de los 120 candidatos tenía publicaciones activas, o sea unos nueve con dominancia cero, y en la Figura 6.2 se ven puntos en el origen. Ahí el logit no existe. ¿Qué se hizo con esos casos?
>
> Lo grave: si se imputa 0,1 % el logit da menos 6,9 y si se imputa 1 % da menos 4,6, y esa diferencia, multiplicada por el coeficiente de 0,111, mueve la predicción de ese candidato unos 25 pp. Es varias veces la mejora de 3,18 pp que se reivindica frente al baseline. Sin declarar la convención, los coeficientes y el MAE no son replicables."

**Acción requerida (CRÍTICO):**
1. Localizar en el código/notebook (03_modelo_continuo.ipynb) qué valor de imputación se usó realmente para los candidatos con dominancia de likes = 0% (aproximadamente 9 de 120 candidatos, dado que solo 92,6% tenía publicaciones activas).
2. Documentar explícitamente esa convención en el texto de 5.6.a (por ejemplo: "a los candidatos sin actividad digital registrada se les imputó una dominancia de X%, correspondiente a [justificación]").
3. Realizar un análisis de sensibilidad mostrando cómo cambian los coeficientes finales y el MAE si se usa una imputación distinta (p. ej. 0,1% vs. 1% vs. un valor basado en el mínimo empírico observado en la muestra), dado que el jurado calculó que esta decisión puede mover la predicción de un candidato hasta ~25 puntos porcentuales — varias veces mayor que la mejora de 3,18pp que el modelo reivindica frente al baseline de proporcionalidad.

---

### 1.14 — Página impresa 22 / PDF p.27 — Capítulo 5, encabezado de Sección 5.6.b "Selección de especificación y regularización (ElasticNet)"

**Comentario textual completo (el comentario más extenso y más crítico de toda la revisión):**
> "Aquí me perdí siguiendo los coeficientes. En 5.6.b y en 6.3.c la especificación queda con 0,111 y 0,026, intercepto 0,258. Dos párrafos después aparece un 0,557 para el moderador que no está en ninguna otra parte, y la Figura 6.4 muestra otro par, 0,423 y 0,221, donde además la dominancia es mayor que la interacción, justo lo contrario de lo que afirma el pie de la figura. El 0,423 se parece demasiado al coeficiente de la regresión fraccional de (5.5), así que sospecho que la figura está graficando otro modelo, pero eso hay que verificarlo. Tal como está, hay tres juegos de números para la misma especificación y la figura contradice al texto.
>
> Y antes de eso hay algo que conviene resolver: ¿los predictores se estandarizaron antes de penalizar? Si no, comparar la dominancia en logit con el producto de esa dominancia por la población centrada no dice mucho, y de esa comparación depende justamente el análisis que se hace en 8.2.
>
> Lo otro es la escala. La sección anuncia enlace logit, pero (5.6) está escrita como un modelo lineal sobre la cuota y (5.7) suma la contribución directamente sobre 0,50. Con la señal de 0,2294 que reporta 5.6.c me da 55,7 % por la inversa del logit y 72,9 % por la regla aditiva, ninguno de los dos es el 60,5 % publicado. Debe faltar un paso intermedio, pero hay que dejarlo escrito.
>
> Sugiero una tabla única con la especificación final, escala de estimación, si hubo estandarización, coeficientes con su dispersión entre pliegues y frecuencia de retención de cada variable, y que texto, figura y conclusiones lean de ahí."

**Acción requerida (MÁXIMA PRIORIDAD — inconsistencia numérica central del trabajo):**

Este es probablemente el punto más importante de resolver antes de la sustentación, porque toca la validez de los números centrales reportados en el Resumen. Pasos concretos:

1. **Volver al notebook 03_modelo_continuo.ipynb** y recuperar el output real y definitivo del ajuste ElasticNet — con sus coeficientes exactos, si hubo o no estandarización previa (StandardScaler antes de ElasticNet), y la escala del enlace usado (logit vs. lineal).
2. **Reconciliar los tres juegos de números que actualmente aparecen en el documento:**
   - Texto en 5.6.b y 6.3.c: β1 = 0.111 (dominancia), β2 = 0.026 (interacción), intercepto = 0.258.
   - Un párrafo después de 5.6.b/6.3.c: β_mod = 0.557 (que no aparece en ningún otro lado del documento y no está claro a qué corresponde).
   - Figura 6.4: coeficientes de 0.423 (dominancia) y 0.221 (interacción), con dominancia > interacción — lo opuesto de lo que dice el pie de figura, y sospechosamente parecido al coeficiente β_logit_likes = 0.4231 de la regresión fraccional de la ecuación 5.5 (Sección 5.6.a), lo que sugiere que **la Figura 6.4 puede estar graficando el modelo equivocado** (el modelo de regresión fraccional simple de 5.6.a, no el ElasticNet final de 5.6.b).
   - Determinar cuál de los tres es el correcto, corregir los otros dos, y regenerar la Figura 6.4 si corresponde.
3. **Aclarar si hubo estandarización de los predictores antes de la penalización ElasticNet.** Si no la hubo, la comparación directa entre el coeficiente de la dominancia en logit y el coeficiente de la interacción dominancia×población-centrada no es directamente interpretable en términos de "cuál pesa más" — esto afecta el argumento central de la Sección 8.2 (Lecciones aprendidas) sobre "la población como moderador, no como efecto directo", que se apoya en que el coeficiente de la interacción es más fuerte que el de dominancia sola.
4. **Resolver la inconsistencia de escala entre 5.6.b, ecuación (5.6), y ecuación (5.7):** la sección anuncia un enlace logit, pero la ecuación (5.6) está escrita como modelo lineal directo sobre la cuota, y la ecuación (5.7) suma la contribución directamente sobre la base de 0.50 (para el caso de dos candidatos). Verificar con el valor concreto: con la señal reportada de 0.2294 (Sección 5.6.c, aplicación a la segunda vuelta 2026), la inversa del logit da 55.7%, mientras que la regla aditiva de (5.7) da 72.9% — **ninguno de los dos coincide con el 60.5% que efectivamente se publica** en el Resumen, Abstract y Sección 6.3.d. Esto indica que falta documentar un paso intermedio en la transformación (posiblemente una re-escala o normalización adicional que sí se hizo en el código pero no quedó explicada en el texto).
5. **Construir la tabla única sugerida por el jurado**: una sola tabla con la especificación final del modelo, la escala de estimación (logit/lineal), si hubo estandarización, los coeficientes con su dispersión entre pliegues de validación cruzada, y la frecuencia de retención de cada variable a través de los pliegues (relevante porque ElasticNet puede eliminar variables en algunos pliegues y no en otros). Todo el texto, las figuras y las conclusiones del documento (especialmente 8.2) deben leer sus números de esta tabla única, para evitar que vuelvan a aparecer números distintos en distintos lugares.

---

### 1.15 — Página impresa 23 / PDF p.28 — Capítulo 5, Sección 5.6.c "Aplicación prospectiva: Segunda Vuelta Presidencial Colombia 2026"

**Fragmento exacto del documento resaltado:**
> "...De la Espriella (22.4 %). Una corrección metodológica fue necesaria para esta aplicación: el modelo fue entrenado en contiendas con un promedio de 3.9 candidatos (intercepto ≈ 0.258, equivalente a una cuota media del 25 % aproximadamente), mientras que una segunda vuelta tiene exactamente dos candidatos y una cuota base del 50 %."

**Comentario textual completo:**
> "Es necesario que quede claro cuál modelo se aplicó, porque el documento dice dos cosas. En 5.6.b la especificación ganadora, con la interacción de población, es la definitiva; en 6.3.c lo que se valida en 2026 es un núcleo agnóstico con el número de candidatos, variable que no quedó retenida y que no está escrita en ninguna parte.
>
> Por otro lado, el 9,43 pp es, según ustedes mismos, el error de la capa municipal, y es el que sostiene el intervalo del pronóstico presidencial aquí, en 6.3.d y en el Resumen. Se está calificando la incertidumbre de un modelo con el error de otro. Si el núcleo agnóstico fue el aplicado, debería estar en la Tabla 6.3 con su propio MAE.
>
> Falta además la fecha de emisión del pronóstico, la ventana de recolección y las plataformas usadas en 2026. Sin eso lo prospectivo no es verificable, y es justo el punto más fuerte que tienen para la sustentación."

**Acción requerida (CRÍTICO — relacionado directamente con 1.14):**
1. Determinar con certeza, revisando el código real usado para generar el pronóstico de la segunda vuelta 2026, cuál de los dos modelos se aplicó realmente:
   - (a) la especificación ganadora completa de 5.6.b (con la interacción dominancia × población-centrada), o
   - (b) el "núcleo agnóstico" mencionado en 6.3.c, que supuestamente incluye el número de candidatos como variable — pero esa variable **no aparece en ningún lado como parte de la especificación final retenida por ElasticNet** (Sección 5.6.b solo retiene dos variables: dominancia y su interacción con población).
2. Si el modelo aplicado en 2026 fue el núcleo agnóstico (sin la variable de población, porque no tiene sentido a nivel nacional), esa especificación **debe aparecer explícitamente en la Tabla 6.3** con su propio MAE fuera de muestra — actualmente la Tabla 6.3 solo muestra: baseline de proporcionalidad, núcleo digital (solo logit_likes), modelo completo ElasticNet, y gradient boosting. Falta la fila correspondiente al modelo efectivamente aplicado en la validación prospectiva.
3. **No se puede seguir usando el MAE de 9.43pp (que es el error del modelo con la capa municipal/población) como el intervalo de incertidumbre del pronóstico presidencial**, si el modelo aplicado en la práctica fue uno distinto (sin esa variable). Hay que recalcular o al menos reportar el MAE del modelo efectivamente usado en 2026, y usar ese valor —no el 9.43— para construir el rango de incertidumbre ("51%–70%") que se menciona en 6.3.d, el Resumen y el Abstract.
4. Agregar a la Sección 5.6.c y/o 6.3.d los siguientes datos de trazabilidad, actualmente ausentes: fecha exacta de emisión del pronóstico (¿cuándo se calculó, antes o después del 21 de junio de 2026?), la ventana de recolección de datos para la segunda vuelta (¿cuántos días antes de la elección?), y las plataformas efectivamente usadas para calcular los 17.087.679 y 4.926.361 likes reportados. Sin esto, la validación prospectiva —que es el resultado más fuerte y más citado del trabajo— no es verificable.

---

### 1.16 — Página impresa 27 / PDF p.32 — Capítulo 6, Sección 6.3.a "Señal digital y correlación con el voto"

**Fragmento exacto del documento resaltado:**
> "Las pruebas U de Mann–Whitney confirmaron que los candidatos ganadores movilizaron, en promedio, más interacciones globales (44.252 vs. 28.011) y un engagement por publicación significativamente mayor (p = 0.0481) que sus contendientes derrotados. La dominancia relativa de likes superó consistentemente al volumen nominal como predictor, con una correlación de Spearman de 0.70 sobre todos los candidatos."

**Comentario textual completo:**
> "Aquí me quedan dudas. La prueba U compara distribuciones, no medias, así que no cubre la diferencia de 44.252 frente a 28.011; el p = 0,0481 es del engagement por publicación. Y asume independencia, cuando los 120 candidatos están anidados en 31 contiendas. Permutando la etiqueta de ganador dentro de cada contienda se resuelve.
>
> Del 0,70 de Spearman: dominancia y cuota son composicionales, así que el número de candidatos mueve las dos y parte de esa correlación es mecánica. Mejor reportarla por contienda o parcializando por número de candidatos.
>
> Faltan dos cosas: la correlación del volumen absoluto, para poder afirmar que la dominancia relativa lo supera, y el intervalo del 71 %, que son 22 de 31 y va de 53 % a 84 %."

**Acción requerida:**
1. Aclarar en el texto que la prueba U de Mann-Whitney (p=0.0481) fue calculada sobre la variable de engagement por publicación, no sobre la diferencia de medias de interacciones totales (44.252 vs. 28.011) — actualmente el párrafo hace parecer que el test estadístico respalda ambas cifras, cuando solo respalda una.
2. Recalcular la significancia estadística teniendo en cuenta que los 120 candidatos no son observaciones independientes (están anidados en 31 contiendas). El jurado sugiere una solución concreta: un test de permutación que mezcle la etiqueta de "ganador/perdedor" **dentro de cada contienda** (no globalmente), para generar una distribución nula que respete la estructura de anidamiento.
3. Sobre la correlación de Spearman de 0.70: reconocer en el texto que dominancia relativa y cuota de voto son variables composicionales (ambas dependen mecánicamente del número de candidatos en la contienda), por lo que parte de esa correlación puede ser un artefacto matemático y no evidencia pura de poder predictivo. Reportar la correlación calculada por contienda (promediando o con un modelo jerárquico), o parcializando por el número de candidatos.
4. Agregar la correlación del volumen absoluto de interacciones (no solo la dominancia relativa) para poder sustentar empíricamente la afirmación de que "la dominancia relativa superó consistentemente al volumen nominal como predictor" — actualmente esta afirmación se hace sin mostrar el número de referencia con el que se está comparando.
5. Agregar el intervalo de confianza del 71% de acierto del heurístico de dominancia (mencionado en 5.5): son 22 aciertos de 31 contiendas, cuyo intervalo de confianza (binomial exacto o de Wilson) va aproximadamente de 53% a 84% — un rango amplio que vale la pena declarar explícitamente en vez de solo reportar el punto estimado.

---

### 1.17 — Página impresa 31 / PDF p.36 — Capítulo 6, Sección 6.3.d "Aplicación a la Segunda Vuelta Presidencial 2026" (cierre de la sección)

**Fragmento exacto del documento resaltado:**
> "...Lo que el modelo reporta correctamente es que la contienda era competitiva: su pronóstico de 60.5 % para Cepeda implica, dentro del intervalo de incertidumbre (± MAE ≈ 9.4 pp), que cualquier resultado entre el 51 % y el 70 % era plausible, y el resultado real (49.52 %) queda a apenas ≈1.5 pp del límite inferior de ese rango (60.5 − 9.43 = 51.07 %)."

**Comentario textual completo:**
> "Ojo con este cierre. El MAE es una medida de exactitud promedio, no de dispersión, así que ± MAE no constituye un intervalo de predicción ni tiene cobertura declarada."

**Acción requerida (CRÍTICO — afecta también el Resumen y el Abstract, que repiten esta misma construcción):**
1. Corregir conceptualmente el uso de "±MAE" como si fuera un intervalo de predicción con una cobertura estadística implícita (p. ej. 68% o 95%). El MAE es una medida puntual de error promedio absoluto, no un cuantil de una distribución de errores, así que "±MAE" no tiene una interpretación probabilística válida sin supuestos adicionales (p. ej. asumir que los errores siguen una distribución simétrica conocida, y aun así el MAE no es directamente la desviación estándar).
2. Si se quiere seguir comunicando un rango de incertidumbre alrededor del pronóstico, usar en su lugar un intervalo empírico basado en la distribución real de errores observados en la validación LOCO-CV (p. ej. percentiles 10 y 90 de los residuos, o un intervalo de predicción bootstrap), y declarar explícitamente qué nivel de cobertura tiene ese intervalo.
3. Esta misma construcción de "±MAE ≈ 9.4pp → rango plausible 51%-70%" aparece repetida en el Resumen y el Abstract del documento — corregir en los tres lugares de forma consistente una vez que se resuelva el punto 1 (además, recordar el punto 1.15: no está claro si 9.43 es siquiera el MAE del modelo correcto que se aplicó en 2026).

---

### 1.18 — Página impresa 32 / PDF p.37 — Capítulo 6, encabezado de Sección 6.4 "Síntesis: contribuciones al estado del arte"

**Comentario textual completo:**
> "Esta sección promete más de lo que muestra el capítulo 6, y contradice un poco la sección 7.3, que está más diplomática. La exportabilidad a otros formatos se apoya en una sola prueba que erró 10,98 pp y no acertó el ganador, y la reconstrucción Weibull está calibrada sobre una única elección, como ustedes mismos reconocen dos páginas después.
>
> En el numeral 1, además, la asimetría temporal es el problema de la Etapa 2, no una de las tres limitaciones que le atribuyeron al SOMEN-DC en 1.2. Conviene ajustar el término.
>
> Y lo del costo me parece lo más importante: en 4.1 y en 5.1.d el costo inferior al de una encuesta es un criterio explícito de viabilidad, pero no hay una sola cifra en todo el documento. Un anexo corto con lo que costaron las suscripciones, el volumen extraído y las horas, contra una referencia de mercado, convertiría este aporte en un resultado verificable.
>
> Último: bajar el tono aquí y en 6.2. "Formidables", "total escalabilidad", "soluciona drásticamente" no ayudan, y contrastan con el análisis de la sección 7.3."

**Acción requerida:**
1. Revisar y moderar el tono general de la Sección 6.4 (Síntesis: contribuciones al estado del arte) para que sea consistente con el tono más cauteloso y matizado de la Sección 7.3 (Limitaciones y trabajo futuro). En particular:
   - El punto 1 de 6.4 ("Elección-Agnosticismo Empírico") habla de "exportar reglas de decisión a elecciones de distinto formato" — esto se apoya en una única aplicación prospectiva (segunda vuelta 2026) que erró 10.98pp y no acertó al ganador. Suavizar la afirmación.
   - El punto 3 de 6.4 ("Restaurador Temporal de Series") describe el modelo Weibull como una solución general, cuando está calibrado sobre una única elección (Costa Rica 2026) — el propio texto lo reconoce dos páginas después en 7.3. Alinear el lenguaje.
2. En el numeral 1 de 6.4, corregir la atribución: la "asimetría temporal" no es una de las tres limitaciones atribuidas al SOMEN-DC en la Sección 1.2 (que son: techo encuestocéntrico, dependencia de infraestructura costosa, y no transferibilidad) — es el problema específico que motivó la Etapa 2 (Costa Rica/Weibull). Ajustar la redacción para no mezclar ambos argumentos.
3. Agregar el anexo de costos sugerido por el jurado: costo real de las suscripciones a Apify/Make.com usadas, volumen de datos extraído, horas invertidas en configuración y mantenimiento del pipeline, comparado con una referencia de mercado del costo de una encuesta tradicional en Colombia. Esto convierte la afirmación de "bajo costo" (mencionada como criterio de viabilidad explícito en 4.1 y 5.1.d) en un resultado verificable, en vez de una afirmación cualitativa sin sustento numérico.
4. Bajar el tono retórico en 6.4 y también en 6.2 (Resultados de Costa Rica): evitar adjetivos como "formidables", "total escalabilidad" y expresiones como "soluciona drásticamente", que contrastan con el análisis más mesurado de la Sección 7.3.

---

### 1.19 — Página impresa 33 / PDF p.38 — Capítulo 7, Sección 7.2 "Impacto práctico"

**Fragmento exacto del documento resaltado:**
> "...consultoría estratégica desplieguen capacidades de inteligencia electoral en tiempo real. En el mediano plazo, estas técnicas se proyectan como la alternativa natural y costo-eficiente frente a los oligopolios demoscópicos, especialmente en otras naciones de Latinoamérica donde la carencia de encuestas sistemáticas o la desconfianza pública en sus resultados exigen métodos de estimación paralelos transparentes y auditables."

**Comentario textual completo:**
> "Publicar estas estimaciones durante campaña, ¿cae o no dentro de la Ley 2494 y su reglamentación del CNE?"

**Acción requerida:** Agregar un párrafo breve en 7.2 (o en las limitaciones de 7.3) abordando explícitamente si el uso práctico de ELA-NOM para publicar estimaciones de intención de voto durante campaña estaría sujeto a la Ley 2494 de 2025 (la misma ley citada en la Sección 1.1 como parte de la motivación del problema, que regula la publicación de encuestas electorales). Esto es relevante porque el capítulo 1 usa las restricciones de esa ley sobre las encuestas tradicionales como argumento a favor de desarrollar alternativas — pero si ELA-NOM también cae bajo el mismo marco regulatorio (por publicar estimaciones de intención de voto durante campaña, aunque no sea técnicamente una "encuesta"), esto afecta directamente el argumento de viabilidad práctica del capítulo 7. Vale la pena investigar la definición legal de "encuesta electoral" en la Ley 2494 y si un modelo basado en redes sociales encajaría en esa definición.

---

### 1.20 — Página impresa 34 / PDF p.39 — Capítulo 8, encabezado de Sección 8.1 "Respuesta a la pregunta de investigación"

**Comentario textual completo:**
> "Falta amarrar objetivos con resultados. El OE4 anuncia clasificación y regresión, y 1.4 y 6.1 lo repiten, pero en el capítulo 6 no hay ningún clasificador; el Top-1 sale de ordenar la regresión, que no es lo mismo. O se incluye, por ejemplo un logit condicional dentro de contienda, o se reformula el objetivo.
>
> La pregunta derivada 4, la del tamaño de muestra, queda sin responder. Una curva de aprendizaje remuestreando subconjuntos de las 31 contiendas la contesta directamente y de paso sustenta lo que hoy se afirma de manera cualitativa sobre el techo predictivo.
>
> De la pregunta 3, la tracción tardía nunca se operacionaliza: no hay ninguna variable temporal en el pool de nueve.
>
> Y el OE2 promete comparación entre modelos de crecimiento, pero la exponencial y la logística se descartan por argumento, sin métricas. Convendría una tabla en 5.4.d.
>
> Último: "como quedó demostrado en la segunda vuelta de 2026" es fuerte para un ensayo que erró 10,98 pp y no acertó el ganador. La misma 7.3 lo dice mejor."

**Acción requerida (afecta Objetivos Específicos OE2 y OE4, y Preguntas derivadas 3 y 4 del Capítulo 2):**

1. **OE4 (Sección 4.2)**: anuncia "entrenar y evaluar modelos de clasificación **y** regresión", y esto se repite en 1.4 y 6.1, pero en el Capítulo 6 nunca se entrena un clasificador binario real — el "Top-1" reportado en la Tabla 6.3 sale de tomar el candidato con mayor cuota predicha por el modelo de regresión, lo cual no es lo mismo que entrenar y evaluar un clasificador. Dos caminos:
   - (a) Incluir efectivamente un modelo de clasificación binaria (el jurado sugiere, por ejemplo, un logit condicional dentro de la contienda — equivalente a un modelo de elección discreta tipo conditional logit de McFadden), o
   - (b) Reformular el OE4 para que refleje honestamente lo que se hizo (solo regresión, con Top-1 derivado).
2. **Pregunta derivada 4** (Capítulo 2, sobre tamaño de muestra necesario para clasificación vs. regresión) queda sin responder empíricamente en el documento. Sugerencia concreta del jurado: una curva de aprendizaje (learning curve) remuestreando subconjuntos de las 31 contiendas disponibles, mostrando cómo cambia el MAE fuera de muestra según el tamaño de la muestra de entrenamiento — esto sustentaría con evidencia lo que hoy solo se afirma de forma cualitativa sobre el "techo predictivo" del modelo dado el tamaño de muestra limitado.
3. **Pregunta derivada 3** (sobre qué métricas digitales son más informativas, incluyendo "capacidad para generar tracción tardía en los últimos días de campaña") nunca se operacionaliza: no existe ninguna variable temporal (p.ej. crecimiento en los últimos 3 días vs. primeros 11 días de la ventana de 14 días) en el pool de 9 variables candidatas evaluado en 5.6.b. Si se quiere responder honestamente esta pregunta derivada, hay que construir al menos una variable de este tipo y evaluarla en el proceso de selección ElasticNet.
4. **OE2** (Sección 4.2, "modelar el crecimiento temporal de las interacciones... de forma comparativa") promete una comparación cuantitativa entre familias de funciones de crecimiento, pero en 5.4.d los modelos exponencial simple y logístico se descartan solo por argumento cualitativo (sin ajustarlos numéricamente ni reportar sus métricas de bondad de ajuste). Sugerencia del jurado: agregar una tabla en 5.4.d con el R² (u otra métrica de ajuste) de las tres familias de funciones evaluadas, para que la elección de la Weibull esté empíricamente sustentada y no solo argumentada cualitativamente.
5. La frase "como quedó demostrado en la segunda vuelta de 2026" (que aparece en la Síntesis 6.4) es una afirmación fuerte para un ensayo prospectivo único que erró 10.98pp y no acertó al candidato ganador. El jurado sugiere alinear el lenguaje de 8.1 con el tono más matizado que ya tiene la Sección 7.3 sobre este mismo resultado.

---

## PARTE 2 — Observaciones de Adrián Santana

> Nota: este documento no tenía anotaciones incrustadas en PDF — es un texto corrido con 5 observaciones numeradas. Se transcriben completas.

### 2.1 — Variable objetivo y alcance inferencial

**Texto completo de la observación:**
> "Conviene precisar si el modelo estima intención de voto en sentido estricto o si aproxima la cuota electoral a partir de señales digitales. Esta distinción es importante porque las interacciones en redes sociales son una variable proxy y pueden reflejar apoyo, visibilidad, polarización, pauta o militancia digital."

**Acción requerida:** Agregar una aclaración conceptual temprana en el documento (posiblemente en la Sección 3.3, "Interacciones digitales como proxy de intención de voto", o en la formalización del problema en 5.1) reconociendo explícitamente que el modelo no mide intención de voto en sentido estricto (una variable actitudinal/psicológica), sino que aproxima la cuota electoral observada a partir de un proxy digital observable. Nombrar explícitamente las fuentes alternativas de varianza que ese proxy puede estar capturando además de apoyo genuino: visibilidad mediática, polarización (que puede generar interacciones negativas o de rechazo, no solo apoyo), pauta publicitaria paga, y militancia digital organizada (posible actividad coordinada no orgánica). Esto conecta directamente con la limitación ya mencionada en 7.3 sobre bots/astroturfing, pero conviene nombrarlo también de forma conceptual más temprano en el documento, no solo como limitación al final.

### 2.2 — Validez predictiva de las interacciones digitales

**Texto completo de la observación:**
> "Aunque se reportan diferencias significativas entre ganadores y perdedores y una correlación de Spearman de ρ = 0.70, sería importante explicar cómo se interpretan estos resultados: una asociación estadística no implica necesariamente capacidad predictiva robusta ni representatividad del electorado. También conviene aclarar si la correlación fue calculada de forma mancomunada y cómo se controla la dependencia entre candidatos de una misma contienda."

**Acción requerida:** Esta observación coincide directamente con el punto 1.16 de Andrés Cruz (Sección 6.3.a). Resolver ambas en conjunto: (a) aclarar explícitamente que la correlación fue calculada de forma mancomunada (pooled) sobre los 120 candidatos, (b) reconocer la limitación de dependencia intra-contienda y aplicar o mencionar una corrección (test de permutación dentro de contienda, sugerido por Cruz), y (c) agregar una frase explícita distinguiendo asociación estadística de capacidad predictiva validada fuera de muestra (que sí se reporta aparte, en la Sección 6.3.b con LOCO-CV) — dejar claro al lector que el ρ=0.70 es evidencia exploratoria/descriptiva, mientras que el MAE de LOCO-CV es la evidencia predictiva real.

### 2.3 — Generalización y validación fuera de muestra

**Texto completo de la observación:**
> "El carácter elección-agnóstico es uno de los aportes centrales del trabajo. Por ello, se recomienda explicar con claridad cómo se validó la capacidad de generalización del modelo, especialmente considerando que el entrenamiento se hace con elecciones locales colombianas y luego se menciona aplicación a una elección presidencial de formato diferente. Sería útil precisar si la validación fue realmente fuera de muestra a nivel de elección y cómo se evita el sobreajuste."

**Acción requerida:** Esta observación conecta directamente con los puntos 1.14 y 1.15 de Andrés Cruz. Aparte de resolver la inconsistencia de coeficientes y de cuál modelo se aplicó en 2026, conviene agregar en el texto (probablemente al inicio de 6.3.d o en un nuevo apartado metodológico) una explicación clara y explícita de:
- Qué significa "fuera de muestra a nivel de elección" en este trabajo — la validación LOCO-CV (Leave-One-Contest-Out) ya hace esto dentro del dataset colombiano (dejando fuera una contienda completa en cada pliegue), pero la aplicación a la presidencial 2026 es un tipo de validación fuera de muestra *distinta y más fuerte*: fuera de muestra a nivel de *tipo de elección* (local vs. nacional/presidencial), no solo a nivel de contienda individual dentro del mismo tipo.
- Cómo se controla el sobreajuste en el proceso de selección de especificación ElasticNet (ya descrito en 5.6.b con la selección anidada, pero conviene resumir esto explícitamente aquí también para que quede claro al lector en el contexto de la pregunta de generalización).

### 2.4 — Interpretación del MAE de 9.43 puntos porcentuales

**Texto completo de la observación:**
> "El resultado supera el baseline de proporcionalidad, lo cual es positivo; sin embargo, un MAE de 9.43 pp sigue siendo amplio para un pronóstico electoral fino. En la sustentación conviene aclarar qué uso práctico permite este nivel de error: si sirve para identificar señales generales, ordenar tendencias o complementar análisis, pero no necesariamente para predecir con precisión resultados cerrados."

**Acción requerida:** Esta observación coincide con el punto 1.17 de Andrés Cruz sobre el mal uso de "±MAE" como intervalo de predicción. Además de la corrección técnica ahí descrita, agregar en la Sección 7.2 (Impacto práctico) o en las Conclusiones un párrafo explícito sobre el uso práctico realista del modelo dado su nivel de error: sirve para identificar tendencias generales y complementar el análisis de campaña, no para predecir con precisión contiendas cerradas — de hecho esto último ya lo reconoce el propio documento en la discusión de la segunda vuelta 2026 (Sección 6.3.d), pero conviene generalizarlo como una afirmación explícita sobre el alcance práctico del modelo, no solo como una explicación ad hoc del resultado de 2026.

### 2.5 — Coherencia entre etapas empíricas y conclusiones

**Texto completo de la observación:**
> "Se recomienda aclarar la relación entre las distintas etapas del trabajo: réplica del modelo SOMEN-DC, reconstrucción temporal mediante Weibull, construcción del dataset colombiano, ElasticNet anidado y aplicación a elecciones de formato diferente. También conviene revisar posibles inconsistencias de redacción, por ejemplo, cuando se menciona Bolivia, Costa Rica, elecciones locales colombianas y segunda vuelta de 2026, para que quede claro qué papel cumple cada caso dentro de la metodología."

**Acción requerida:** El documento ya tiene una Sección 1.4 ("Estructura del documento") y una Sección 5.2 ("Diseño general del proceso") que explican en general la relación entre las etapas, pero según esta observación no queda suficientemente clara para el lector. Sugerencias:
- Considerar agregar un diagrama de flujo simple (Bolivia → Costa Rica → Colombia → Aplicación 2026) mostrando qué pregunta de investigación resuelve cada etapa (esto ya está esbozado en el texto de 5.1.d: "El ejercicio de Bolivia ayudó a solucionar las preguntas P1 y P2, mientras que el ejercicio de Costa Rica y de Colombia ayudó a solucionar la pregunta P3... la pregunta P4 se puede resolver con los resultados del ejercicio con la Segunda Vuelta...") — convertir esta explicación textual en un elemento visual explícito ayudaría a la claridad.
- Revisar consistencia terminológica: asegurarse de que en todo el documento se llame igual a cada etapa (ej. "Etapa 1 - Bolivia", no a veces "ejercicio de Bolivia", a veces "caso de estudio", etc.) y que las transiciones entre secciones expliquen siempre de forma explícita por qué se pasa de una etapa a la siguiente.

---

## PARTE 3 — Resumen ejecutivo de prioridades

Para facilitar el trabajo del agente que hará las correcciones, este es el orden de prioridad sugerido:

### Prioridad 1 — Bloqueantes (afectan la validez numérica reportada en Resumen/Abstract)
- 1.14 — Tres juegos de coeficientes distintos para el modelo final ElasticNet.
- 1.15 — Cuál modelo se aplicó realmente en la validación 2026, y de qué modelo es el MAE=9.43 usado como intervalo.
- 1.17 / 2.4 — Uso incorrecto de "±MAE" como intervalo de predicción.
- 1.12 — Sesgo de selección: filtro de 10.000 votos y exclusión de Bogotá.
- 1.13 — Imputación de dominancia cero (logit indefinido).

### Prioridad 2 — Importantes, requieren trabajo analítico pero son defendibles con buena explicación
- 1.6 — Interpretación de parámetros Weibull (k, α, t0).
- 1.16 / 2.2 — Pruebas estadísticas (Mann-Whitney, Spearman) sin controlar dependencia intra-contienda.
- 1.4 / 1.5 — Inconsistencia de dominio/codominio de f entre Capítulo 1 y Capítulo 3.
- 1.20 — Desajuste entre objetivos específicos (OE2, OE4) y lo efectivamente reportado en resultados.
- 1.11 — Falta de anexo de reproducibilidad (repositorio, versiones, semillas).
- 2.3 — Explicar con más claridad el diseño de validación fuera de muestra.

### Prioridad 3 — Menor esfuerzo, pulido de forma
- 1.1 — Formato de citas, separadores decimales/miles, índices de figuras/cuadros/siglas.
- 1.2 — Comparación no homogénea de cifras de mercado (facturación vs. volumen transado).
- 1.3 — Base de cálculo de cifras de penetración de redes sociales (DataReportal).
- 1.7 / 1.8 — Notación de intención de voto y ecuación de suma de votos.
- 1.9 — MAE=RMSE en Tabla 6.1 por tratarse de n=1.
- 1.10 — Inconsistencia entre texto e Instagram en Tabla 6.2 (umbral del 20%).
- 1.18 — Tono retórico en Secciones 6.2 y 6.4.
- 1.19 — Pregunta legal sobre Ley 2494.
- 2.1 — Aclaración conceptual sobre qué mide realmente el proxy digital.
- 2.5 — Claridad narrativa sobre el rol de cada etapa empírica.
