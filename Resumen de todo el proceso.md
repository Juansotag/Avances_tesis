#

Secretario > lina > Ivon > Zulma > Otto/Viviana/Gina

## ** 1. Justificación**

En este momento, en Latinoamér3ica no existen herramientas de seguimiento de la intención de voto durante elecciones más allá de las encuestas, las cuales, tanto por coyuntura interna en Colombia como por intervención y sesgo de los encuestadores, no son una representación fidedigna o insesgada de la intención de voto (Ver lo escrito por Andrés Caballero, director de Cifras y Conceptos), por lo tanto se hace necesario desarrollar herramientas novedosas para el pronóstico de la intención de voto. En este proyecto se busca desarrollar y probar una metodología para el estimación de la intención de voto.

Ya existen metodologías que usan ciencia de datos y fuentes abiertas como redes sociales para realizar estos pronósticos,  pero estos presentan ciertas dificultades que este proyecto busca solucionar. Esta metodología busca:

- No utilizar encuestas para su funcionamiento
- Ser elección-agnóstica: esto significa que los pesos y parámetros del modelo puedan ser aplicables a más de una elección y que se entrenen con varias elecciones.
- No necesite levantar datos durante las elecciones para ser utilizado, por lo que pueda usar datos de elecciones anteriores 

## **2. Contexto**

Esto presenta una mejora frente a modelos actuales de machine learning que usan redes sociales, como el modelo de *nowcasting* SOMEN-DC, desarrollado por Brito y Andeoato, de la Universidad Federal de Pernambuco en el Brasil que usa encuestas e interacciones en redes sociales recopiladas durante la campaña electoral, y otros modelos que utilizan las interacciones de ciudadanos comunes y corrientes. Estos últimos implican el manejo de grandes cantidades de datos recopilados durante la campaña electoral, mucho más que el modelo SOMEN-DC.

Este modelo fue el escogido para intentar aplicarlo al contexto latinoamericano, pero, al hacer una revisión más a profundida de su metodología se encontraron un conjunto de errores y dificultades metodológicas que hacían tanto su implementación como replicación difíciles: 

El modelo SOMEN-DC funciona calculando variables del número de interacciones totales de las publicaciones a tiempos regulares, con esto, se entrena un modelo específico para cada elección, usando las encuestas como variable objetivo. Esto plantea varios problemas metodológicos:

- Los modelos no tienen forma de tener una mejor capacidad predictiva que las elecciones (su objetivo) más allá del error respecto a las encuestas.
- Es necesario hacer un seguimiento durante las elecciones que puede ser computacionalmente pesado, Brito y Andeoato tenían acceso a servicios de Web scrapping institucionales que hoy en día no existen. Ellos parece que pueden conocer cuantas interacciones tiene cada publicación de cada candidato y como aumenta día a día gracias a servicios propios de su universidad. Esos servicios no lo tiene mi universidad porque se volvieron muy costos y ya no existen
- Los modelos no toman información de otras elecciones y solo son similares o mejores que las encuestadoras en ciertos casos. 

