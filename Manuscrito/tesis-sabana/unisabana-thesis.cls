% =============================================================
%   LaTeX thesis template — Universidad de La Sabana
%   Adaptado de unipd-thesis-modern por Francesco Barone
%   github.com/baronefr/unipd-thesis-modern
%
%   Adaptación: Juan Sotelo Aguilar, 2026
%   Maestría en Analítica Aplicada
%   Universidad de La Sabana, Colombia
%
%   Colores institucionales:
%     Azul Sabana: RGB(26, 47, 111)  → #1A2F6F
% =============================================================

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{unisabana-thesis}[Tesis Universidad de La Sabana]


% -- CLASE BASE --
\LoadClass[11pt, a4paper, oneside, openany]{book}

\RequirePackage{etoolbox}
\makeatletter
\patchcmd{\chapter}{\if@openright\cleardoublepage\else\clearpage\fi}{\par\vspace{1cm}}{}{}
\makeatother

% -- MÁRGENES --
\RequirePackage[
  twoside, a4paper,
  inner=35mm, outer=25mm,
  top=27mm, bottom=27mm,
  headsep=5mm, headheight=14pt,
  footskip=11mm,
  marginparwidth=0mm, marginparsep=0mm,
]{geometry}

\RequirePackage{scrextend}
\RequirePackage[explicit]{titlesec}


% -- FUENTES --
\RequirePackage[T1]{fontenc}
\RequirePackage{newpxtext}


% -- IDIOMA: ESPAÑOL --
\RequirePackage[spanish, es-nodecimaldot]{babel}
\RequirePackage[utf8]{inputenc}


% -- PAQUETES ÚTILES --
\RequirePackage{url}
\RequirePackage{graphicx}

% Colores
\RequirePackage[table]{xcolor}
    % Color institucional Universidad de La Sabana
    \definecolor{sabanaBlue}{RGB}{26, 47, 111}
    \colorlet{mainColor}{sabanaBlue}
    \colorlet{chapterColor}{sabanaBlue}
    \colorlet{partBoxColor}{sabanaBlue}
    \colorlet{generalHyperColor}{sabanaBlue}

% Matemáticas
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage[makeroom]{cancel}

% Apéndices
\RequirePackage{appendix}

% Espaciado
\RequirePackage{setspace}
\addtolength{\footnotesep}{1mm}

\makeatletter
\setlength{\@fptop}{0pt}
\makeatother

\setlength{\parindent}{11pt}

% Leyendas y notas al pie
\RequirePackage[font=small, labelfont=bf]{caption}
\RequirePackage{subcaption}
\RequirePackage{footnote}
\RequirePackage[bottom]{footmisc}

\makeatletter
\renewcommand{\footnoterule}{%
  \begin{tikzpicture}[remember picture,overlay]
    \fill[sabanaBlue] (current page.west |- 0,1em) rectangle (current page.south east);
  \end{tikzpicture}%
}
\let\oldmakefntext\@makefntext
\renewcommand{\@makefntext}[1]{%
  \color{white}\oldmakefntext{#1}%
}
\makeatother

% Filigranas / marca de agua
\RequirePackage{watermark}

% Diagramas TikZ
\RequirePackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta}

% Bibliografía
\RequirePackage[autostyle]{csquotes}
\RequirePackage[backend=biber, style=apa, sortcites=true]{biblatex}

% Tablas
\RequirePackage{tabularx}
\RequirePackage{multirow}
\RequirePackage{booktabs}

% Bucles (para logos)
\RequirePackage{pgffor}

% Código fuente
\RequirePackage{listings}
\lstset{
  basicstyle=\ttfamily\small,
  keywordstyle=\color{sabanaBlue}\bfseries,
  commentstyle=\color{gray},
  stringstyle=\color{teal},
  breaklines=true,
  frame=single,
  numbers=left,
  numberstyle=\tiny\color{gray},
}

% Hipervínculos (cargado después por pdfx)
% \RequirePackage{hyperref}


% -- DEFINICIONES DE METADATOS --
\makeatletter
\def\thesisHeader#1{\gdef\@thesisHeader{#1}}
\def\programa#1{\gdef\@programa{#1}}
\def\annoAcademico#1{\gdef\@annoAcademico{#1}}
\def\cedula#1{\gdef\@cedula{#1}}
\def\secondpage#1{\gdef\@secondpage{#1}}
\def\dedication#1{\gdef\@dedication{#1}}

% Directores
\def\director#1#2{\gdef\@director{#1} \gdef\@directorInst{#2}}
\def\codirector#1#2{\gdef\@codirector{#1} \gdef\@codirectorInst{#2}}

\makeatother

% Valores por defecto vacíos
\codirector{}{}
\secondpage{}
\dedication{}


% -- LISTAS Y ENUMERACIONES --
\let\saveditemize=\itemize
\let\savedenditemize=\enditemize
\renewenvironment{itemize}
    {\begin{spacing}{1.0}\saveditemize\itemsep0em }
    {\savedenditemize\end{spacing}}

\let\savedenumerate=\enumerate
\let\savedendenumerate=\endenumerate
\renewenvironment{enumerate}
    {\begin{spacing}{0.5}\savedenumerate}
    {\savedendenumerate\end{spacing}}

\let\savedquote\quote
\let\endsavedquote\endquote
\renewenvironment{quote}
    {\itshape\savedquote}
    {\endsavedquote}


% -- CABECERAS Y PIES DE PÁGINA --
\RequirePackage{fancyhdr}
\RequirePackage[explicit]{titlesec}

% Estilo de parte
\titleformat{\part}[display]
  {\centering}
  {}
  {0pt}
  {%
    \vspace*{\fill}
    \vspace*{-9cm}
    \setlength{\fboxsep}{5pt}
    \colorbox{partBoxColor}{\color{white}\LARGE\bfseries \partname~\thepart}\\
    \vspace{0.8cm}
    {\Huge\bfseries #1}
    \thispagestyle{empty}
    \vspace*{\fill}
  }

% Estilo de capítulo
\newcommand*\chapterlabel{}
\titleformat{\chapter}[display]
	{\normalfont\bfseries\Huge}
	{\gdef\chapterlabel{\thechapter}}
 	{0pt}
 	{%
      \begin{tikzpicture}[remember picture,overlay]
        \coordinate (leftedge) at (current page.west |- 0,0);
        \fill[chapterColor] (leftedge) ++(0, 10mm) rectangle ++(35mm, -16mm);
        \node[anchor=base east] at ([xshift=31mm]leftedge) {\color{white}\bfseries\Huge\chapterlabel};
      \end{tikzpicture}%
      \hspace*{20mm}\parbox[t]{\dimexpr\textwidth-20mm\relax}{\raggedright #1}%
      \gdef\chapterlabel{}%
    }

% Capítulo sin número
\titleformat{name=\chapter,numberless}[display]
	{\normalfont\bfseries\Huge}
	{}
 	{0pt}
 	{%
      \begin{tikzpicture}[remember picture,overlay]
        \coordinate (leftedge) at (current page.west |- 0,0);
        \fill[chapterColor] (leftedge) ++(0, 10mm) rectangle ++(35mm, -16mm);
      \end{tikzpicture}%
      \hspace*{20mm}\parbox[t]{\dimexpr\textwidth-20mm\relax}{\raggedright #1}%
    }

\renewcommand{\headrulewidth}{0pt}
\titlespacing*{\chapter}{0pt}{0pt}{1cm}
\renewcommand{\thesubsection}{\thesection.\alph{subsection}}

\newcommand{\setDefaultHF} {
    \fancyhf{}
    \fancyhead[L]{{\bfseries\footnotesize\leftmark}}
    \fancyfoot[C]{%
      \begin{tikzpicture}[remember picture,overlay]
        \fill[sabanaBlue] (current page.south west) rectangle ([yshift=1.5cm]current page.south east);
        \node at ([yshift=0.75cm]current page.south) {\color{white}\bfseries \thepage};
      \end{tikzpicture}%
    }
}


% -- TABLA DE CONTENIDO --
\RequirePackage[titles]{tocloft}
\setlength{\cftbeforesecskip}{2pt}
\setlength{\cftbeforepartskip}{2em}


% -- FRONTMATTER --
\fancypagestyle{plain}{%
    \fancyhf{}
    \fancyfoot[C]{%
      \begin{tikzpicture}[remember picture,overlay]
        \fill[sabanaBlue] (current page.south west) rectangle ([yshift=1.5cm]current page.south east);
        \node at ([yshift=0.75cm]current page.south) {\color{white}\bfseries \thepage};
      \end{tikzpicture}%
    }
    \renewcommand{\headrulewidth}{0pt}
}

\renewcommand{\frontmatter} {
    \pagenumbering{roman}
    \pagestyle{fancy}

    \maketitle
    \secondcoverpage
    \clearpage

    \pagestyle{plain}
    \setlength{\headwidth}{\textwidth}

    \def\abstractname{Abstract}
    \def\resumenname{Resumen}
    \def\acknowledgmentsname{Agradecimientos}

    \dedicationpage

    {\hypersetup{linkcolor=black}%
    \titlespacing*{\chapter}{0pt}{0pt}{1.5cm}%
    \tableofcontents}
    \clearpage

    \abstractpage
}


\newcommand{\printlogos}[2][2cm]{
    \foreach \x [count=\xi] in {#2}
       { \hspace{5mm}\includegraphics[height=#1]{\x} }
}


% ============================================================
% -- PORTADA (maketitle adaptada para La Sabana) --
% ============================================================
\makeatletter
\renewcommand{\maketitle} {

    \newgeometry{
        top=2cm, bottom=2cm,
        inner=4cm, outer=2cm,
        headheight=0cm,includehead,includefoot
    }

    \fancyhf{}
    \thispagestyle{empty}

    % Fondo institucional sutil (barra azul en la parte lateral izquierda)
    \begin{tikzpicture}[remember picture, overlay]
        \fill[sabanaBlue!8] (current page.south west) rectangle (current page.north east);
        \fill[sabanaBlue] (current page.south west) rectangle ([xshift=30mm]current page.north west);
    \end{tikzpicture}

    % Logo Universidad de La Sabana
    {\noindent\includegraphics[height=2.2cm]{template/unisabana-logo}}

    % Línea separadora
    \vspace{3mm}
    {\color{sabanaBlue}\rule{\linewidth}{1.5pt}}
    \vspace{1mm}

    % Encabezado del programa
    \begin{flushleft}
    \vspace{4ex}
    {\large\textsc{\color{sabanaBlue}\@thesisHeader}}

    % Título
    \vspace{10ex}
    \begin{spacing}{1.2}
    \noindent\LARGE\textbf{\@title}
    \end{spacing}
    \end{flushleft}

    % Autor
    \vspace{2cm}
    \begin{flushleft}

        {\Large\textbf{\@author}}

    % Director
    \vspace{3cm}
    \begin{minipage}[t]{7cm}
        \textsc{\color{sabanaBlue}Director}\\
        \vspace{1.5mm}
        {\large\textbf{\@director}}\\
        \vspace{0.5mm}
        {\normalsize\@directorInst}
    \end{minipage}%
    \begin{minipage}[t]{7cm}
      \ifx\@codirector\empty \else
        \textsc{\color{sabanaBlue}Codirector}\\
        \vspace{1.5mm}
        {\large\textbf{\@codirector}}\\
        \vspace{0.5mm}
        {\normalsize\@codirectorInst}
      \fi
    \end{minipage}

    \end{flushleft}

    \vspace*{\fill}
    \begin{flushleft}
    \large\textsc{Año Académico \@annoAcademico}
    \end{flushleft}
    \vspace{5mm}

    \restoregeometry
}
\makeatother


% -- DEDICATORIA --
\makeatletter
\newcommand{\dedicationpage} {
\ifx\@dedication\empty \else
    \thispagestyle{empty}
    \vspace*{2cm}
    \phantomsection
    \begin{flushright}
    \@dedication
    \end{flushright}
    \clearpage
\fi
}

% -- SEGUNDA PÁGINA DE CUBIERTA --
\newcommand{\secondcoverpage} {
\ifx\@secondpage\empty \else
    \phantomsection
    \@secondpage
\fi
}
\makeatother


% -- ABSTRACT / RESUMEN --
\newenvironment{abstract}[1][es] {
    \def\es{es}
    \def\arg{#1}

    \thispagestyle{plain}

    \ifx\arg\es
    \phantomsection
    \addcontentsline{toc}{chapter}{\resumenname}
        \section*{\LARGE\resumenname}
    \else
    \phantomsection
    \addcontentsline{toc}{chapter}{\abstractname}
        \section*{\LARGE\abstractname}
    \fi
} {
    \vspace{1cm}
}

\newcommand{\abstractpage} {
    \input{docs/resumen}
    \vspace{1cm}
    \input{docs/abstract}
}


% -- MAINMATTER --
\renewcommand{\mainmatter} {
    \vspace{1cm}
    \pagestyle{fancy}
    \setDefaultHF
    \renewcommand{\headrulewidth}{1pt}

    \setcounter{page}{1}
    \pagenumbering{arabic}
    \setcounter{chapter}{0}

    \setstretch{1.1}
}


% -- AGRADECIMIENTOS --
\makeatletter
\newcommand{\acknowledgments} {
  \chapter*{\acknowledgmentsname}
  \markboth{\acknowledgmentsname}{}
  \input{docs/agradecimientos}
}
\makeatother


% -- GLOSARIO / ACRÓNIMOS --
\RequirePackage[acronym, toc, nonumberlist]{glossaries}
\makeglossaries


% -- BACKMATTER --
\renewcommand{\backmatter}{
    \bookmarksetup{startatroot}

    % Glosario (si se usa)
    % \begingroup
    % \let\clearpage\relax
    % \printglossaries
    % \endgroup

    % Referencias
    \clearpage
    \phantomsection
    \addcontentsline{toc}{chapter}{\bibname}
    \printbibliography
}


% -- EXPORTAR COMO PDF/A --
\RequirePackage{etoolbox}
\RequirePackage{silence}
\WarningFilter{pdfx}{Setting all color commands to rgb}
\RequirePackage[a-2b]{pdfx}

\hypersetup{
  colorlinks=true,
  citecolor=generalHyperColor,
  filecolor=black,
  linkcolor=generalHyperColor,
  urlcolor=generalHyperColor,
  pdfborder={0 0 0}
}

\RequirePackage{bookmark}
