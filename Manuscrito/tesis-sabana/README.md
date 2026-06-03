# Tesis — Universidad de La Sabana

**Título:** Diseño e implementación de un modelo de *nowcasting* elección-agnóstico
para la intención de voto aplicado a elecciones locales en Colombia

**Autor:** Juan Sotelo Aguilar  
**Programa:** Maestría en Analítica Aplicada  
**Universidad:** Universidad de La Sabana  
**Año:** 2026

---

## Estructura del proyecto

```
tesis-sabana/
│
├── main.tex                  ← Archivo principal (compilar este)
├── unisabana-thesis.cls      ← Clase LaTeX personalizada (no modificar)
├── custom-symbols.tex        ← Atajos matemáticos y de texto propios
├── refs.bib                  ← Bibliografía en formato BibTeX
├── README.md                 ← Este archivo
│
├── chapters/                 ← Un archivo .tex por capítulo
│   ├── introduccion.tex
│   ├── marco-conceptual.tex
│   ├── metodologia.tex       ← (crear cuando corresponda)
│   └── resultados.tex        ← (crear cuando corresponda)
│
├── docs/                     ← Páginas especiales
│   ├── resumen.tex           ← Resumen en español
│   ├── abstract.tex          ← Abstract en inglés
│   ├── agradecimientos.tex
│   └── glosario.tex
│
├── img/                      ← Imágenes y figuras
│   └── (agregar aquí tus figuras)
│
└── template/                 ← Recursos de la plantilla (no modificar)
    ├── unisabana-logo.png    ← Logo Universidad de La Sabana
    └── extras.tex
```

---

## Cómo compilar

### Opción 1: LaTeX Workshop en Antigravity / VS Code

1. Instala TeX Live (Mac/Linux) o MiKTeX (Windows)
2. Instala la extensión **LaTeX Workshop**
3. Abre `main.tex` → guarda → el PDF se genera automáticamente

El orden de compilación correcto es:
```
pdflatex → biber → pdflatex → pdflatex
```
LaTeX Workshop lo hace automáticamente con la receta `latexmk`.

### Opción 2: Terminal (manual)

```bash
cd tesis-sabana
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

---

## Cómo agregar un capítulo nuevo

1. Crea el archivo en `chapters/mi-capitulo.tex`  
2. Empieza con `%!TEX root = ../main.tex` en la primera línea  
3. Agrega `\input{chapters/mi-capitulo}` en `main.tex`

---

## Cómo citar

Las referencias están en `refs.bib`. Para citar usa:

```latex
\cite{lewisbeck2011nowcasting}         % cita básica: (Lewis-Beck et al., 2011)
\citeauthor{tumasjan2010}              % solo el autor: Tumasjan et al.
\citeyear{tumasjan2010}               % solo el año: 2010
\parencite{brito2023somen}            % entre paréntesis: (Brito & Adeodato, 2023)
```

---

## Colores institucionales

La clase usa el **azul La Sabana** `RGB(26, 47, 111)` definido como `sabanaBlue`.  
Para usarlo en el texto: `\textcolor{sabanaBlue}{texto}`.

---

## Notas sobre la clase

La clase `unisabana-thesis.cls` está basada en `unipd-thesis-modern` de Francesco Barone
([github.com/baronefr/unipd-thesis-modern](https://github.com/baronefr/unipd-thesis-modern)),
adaptada para la Universidad de La Sabana con:
- Idioma en español (`babel`)
- Color azul institucional
- Logo de La Sabana en portada
- Terminología en español (Director, Resumen, Agradecimientos, Año Académico)
- Estilo de bibliografía APA (`biblatex-apa`)
