# Learning log

## 2026-10-15 · 3 h
- Hice: instalé Git, creé el repositorio, escribí el acta, determiné y creé el environment con conda-forge y las dependencias necesarias para las tareas que se realizarán, determiné la estacion de medicion de caudales a utulizar (revisando la existencia de datos historicos para su uso posterior).
- Aprendí: qué es un repositorio, add / commit / push, qué es un project charter, como registrar decisiones y aprendizajes en el repo, como crear un environment para el proyecto y que dependencias escoger segun las tareas que se realizarán. 
- No entendí: -
- Ayuda de IA: Guia sobre como crear el repo y como ir actualizándolo gradualmente.

## 2026-10-16 · 8 h
- Hice: 
    - Abrí el Excel del SNIH en Python y verifiqué tipos, fechas y cantidad de filas. Con eso se cumplió la puerta de la fase 0.
    - Controles de calidad: días esperados vs. reales (103 faltantes, 0,40%), sin valores ≤ 0 ni fechas duplicadas.
    - Ubiqué los huecos con un calendario completo: 3 bloques largos en invierno (1962, 1976, 1985) y 3 días sueltos.
    - Rellené los huecos con interpolación lineal y una bandera filled para marcar los días interpolados (D4).
    - Grafiqué la serie diaria de 70 años con los días interpolados en rojo.
    - Calculé promedios anuales y por década, la mediana como umbral de año seco y las rachas de años secos (D5).
    - Estructuré el notebook en secciones 1.0 a 1.5 con markdowns e interpretación.
    - Commits: notebook + D4; gráfico + análisis + D5; formato de DECISIONS.md.
- Aprendí:
    - Notebook: celda, kernel, celdas Markdown vs. código, rutas relativas (../), por qué solo la última línea se muestra sola, display().
    - pandas: DataFrame y Series, read_excel con skiprows, to_datetime con format, .dt.normalize(), info(), head(), set_index, reindex, date_range, isin / difference, interpolate, groupby, median, indexación booleana, .loc, .tolist(), etc.
    - Python: f-strings, que los métodos de pandas devuelven un objeto nuevo (hay que asignarlo), división entera //, .round() vs. round().
    - Método: un chequeo tiene que poder fallar; los promedios anuales solo valen con años completos; pico ≠ año húmedo (crecida vs. volumen); mediana vs. promedio; las rachas de años secos importan más que un año seco aislado (H1); año hidrológico (julio-junio del SNIH vs. octubre-septiembre del DGI, pendiente para D6).
    - Herramientas: 1) Git: CRLF vs. LF; git restore. ; 2) Windows: un entorno de conda no activado puede tirar el kernel; 3) Markdown
- Resultados importantes:
    - Mediana anual: 40,6 m³/s.
    - Años más húmedos: 1983 y 1987.
    - Año más seco: 1971.
    - Rachas secas: 2010-2015 y 2018-2023 (6 años cada una); 1957-1972 tuvo 15 años secos de 16.
    - Conclusión: las rachas secas son recurrentes en este río.
- No entendí:
    - Funcionamiento completo del kernel y la importancia de la activacion del entorno.
- Ayuda de IA:
    - El diagnóstico del kernel caído (activación del entorno).
    - La tabla de huecos por bloque y la recomendación de interpolar (D4).
