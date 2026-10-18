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

## 2026-10-17 · 5 h
- Hice: 
    - El kernel de VS Code volvio a caerse. Dos razones posibles:
     - Estaba en restricted mode
     - Estaba haciendo modificaciones sobre la copia (checkpoint)
    - Para resolver la caida del kernel: Trust folder, activar environment hydro y run all. 
    - Se propuso el interrogante: Quedan 69 en vez de 70, lo que llevó a D6
    - D6: Año hidrologido de octubre a septiembre, etiquetando por el año en que termina segun la convecion de DGI.Quedan entonces 69 años completos (1957-2025)
    - Se corre nuevamente el analisis para exclusivamente años secos con años hidrologicos (1.6):
     - Mediana : 40.8 m3/s
     - 10 de 69 años cambian de categoria respecto del año calendario
     - Se identificaron distintas rachas de años secos
    - Se inicio 1.7: Curva de duracion de caudales con formula de Weibull y escala logaritmica para visualizar datos. Determinacion de cuantiles: Q10 91.5, Q30 47.4, Q50 29.9, Q90 16.7 m3/s.
    - Q10/Q90 = 5.5, Q10 no significa crecidas y Q90 no significa sequias. Es necesario separar el concepto de variacion estacional con interanual.
    - Caudal de diseño fijado entre Q30 y Q40. Operación a carga parcial y vertido del excedente. Funcionamiento de turbina hidroelectrica y su comportamiento frente caudales superiores e inferiores al de diseño.
    - Caudal mínimo técnico de la Francis (aprox. 50%): con Q90 llega 35% con una unidad y 70% con dos unidades iguales. Barajar la posibilidad de poner dos turbinas que juntas sumen al caudal de diseño, esta decision tiene implicancias en parametros como CAPEX, mantenimiento, etc. 

- Aprendí:
    - Workspace Trust y .ipynb_checkpoints.
    - Fortalecí concepto de año hidrologico, variacion interanual y variacion estacional
    - FDC y excedencia: la FDC pierde totalmente la secuencia cronológica (Searcy 1959).
    - Segun el caudal que recibe la turbina se tiene casos de: Carga parcial y vertido.
    - Caudal mínimo técnico; ventaja operativa de dos unidades frente a su costo en CAPEX.
    
- Ayuda de IA:
    - La reparación de VS Code respecto al problema del kernel, ayuda con la consola de conda para inicializar bien el entorno.
    - Bloque de código para graficar la FDC. Parametros para que la curva se vea clara y con escala logaritmica para su visualizacion.
    - Búsqueda de las fuentes para llegar a los metodos mas usados en estos casos.

## 2026-10-18 · 5 h
- Hice: 
    - Recuperación del trabajo “perdido”: VS Code había restaurado una versión vieja en memoria. Primero commit desde el disco y después File: Revert File.
    - Correcciones sobre markdowns para explicar bien los procedimientos:
     - Los cuantiles salen de los datos de pandas y no de Weibull
     - Agregar fuentes
     - Salvedad de costos en las dos unidades, importante para las fases futuras
    - Calculo de caudal ecologico con Tennant(1975): 10% del caudal medio anual = 4.4 m3/s. Permitio crear la serie q_available
    - Bug en .clip
    - Caudal de diseño q_available ya definido: Q30 = 43.0 m3/s, dos unidades de 21.5. Con Q90 queda en 57% y con Q95 en 52%. 
    - Tramos de operación: período completo contra años secos (30/29/37.5/3.5% contra 20.2/23.8/48.9/7.1%) y días por año (13 contra 26 bajo el mínimo)
    - Errores:
     - Usar los promedios anuales en vez de los valores de los dias
     - Recalcular caudal ecologico y diseño para años secos. Es exactamente el mismo caudal de diseño para ambos casos, solo cambian los dias de comparacion
     - Contadores acumulativos que debian ser definidos inicialmente
    - Interpretacion:
     - Puntos porcentuales contra cambio relativo
     - Cantidad de días no es lo mismo que energía
     - Plantear hipótesis de la brecha P50/P90, a confirmar en fases posteriores
    - D7 (caudal ecológico)

- Aprendí:
    - Caudal ecológico y Tennant; inversión de estaciones en el hemisferio sur.
    - Por qué el diseño se hace sobre el caudal disponible.
    - Umbrales de operación por caudal, no por percentiles.
    - El kernel guarda estado entre corridas: por qué conviene Run All.
    - Puntos porcentuales contra cambio relativo.

- Ayuda de IA:
    - Diagnostico de buffer viejo en VScode
    - Verificación independiente de todos los resultados.

