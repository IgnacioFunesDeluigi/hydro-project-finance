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

## 2026-10-19 · 5 h
- Hice: 
    - Hoja de ruta de lo que queda de la fase 1, de la 1.9 a la 1.13.
    - 1.9: salto y turbina.
     - Ecuación de potencia. Salto neto requerido: H = 26.9 m, con 10 MW, 43.0 m3/s y η = 0.88.
     - Encontrar fuente de ESHA (Tabla 3-2) con el mínimo técnico de cada turbina y se hizo la verificacion.
     - Comparacion de tres configuraciones por días bajo el mínimo técnico:
                    | Config | Complete period | Dry years |
                    | :--- | :---: | ---: |
                    | A (2×Francis) | 3.5% | 7.1% |
                    | B (1×Kaplan) | 0.05% | 0.1% |
                    | C (2×Kaplan) | 0.0% | 0.0% |

     - Bug: los contadores de años secos usaban el contador del período completo.
     - Primera propuesta de D8 con Francis, se reformuló y seleccionó B: 1 Kaplan de 43 m3/s.
     - En D8 se corrigió la limitación de CAPEX.
    - Investigación: cómo modelar η. La respuesta fue curvas de fabricante o de guía e interpolación, no regresión.
    - 1.10: potencia y energía diaria
     - q_turbined con .clip() y .where().
     - Tres controles: 10 MW, 30% de días a plena potencia y 13 días en cero.
    - 1.11: energía anual, P50, P90 y factor de planta
     - Primer intento agrupado por año calendario: dio 70 años, con 1956 y 2025 parciales.
     - Resultado final: P50 = 57.1 GWh, P90 = 45.0 GWh, P90/P50 = 0.79, factor de planta de 65% (P50) y 51% (P90).
     - Los 7 años bajo el P90 son años secos y 6 están dentro de rachas, lo que apoya H1.
    - Visión global: fase 1 al ~85%, adelantada en calendario y excedida en horas.


- Aprendí:
    - Salto bruto contra neto; eficiencia (USBR ~90%); clasificación de salto bajo (<30 m, ESHA).
    - Caudal mínimo técnico por tipo de turbina; Kaplan contra Francis a carga parcial.
    - Límite del modelo: con η constante no se distinguen B y C. Redundancia y disponibilidad.
    - Potencia (MW) contra energía (MWh, GWh); compatibilidad de unidades en el factor de planta.
    - Controles que dan bien “por construcción”: verifican el código.
    - P50 y P90 como excedencia; mediana contra media.
    - Variabilidad estacional (Q10/Q90) contra interanual (P90/P50); persistencia de los años malos.
    - pandas: .clip, .where, groupby por año hidrológico, .describe(), formato :.1%, axhline y legend.
- No entendí:
    - Nada pendiente
- Ayuda de IA:
    - La estructura de la D8.
    - El texto completo del markdown de concepto y de la interpretación de la 1.11.
    - Las explicaciones de por qué el modelo no distingue B de C y de cómo se modela η variable.
    - Verificación independiente de resultados.

## 2026-10-20 · 7 h
- Hice:
 - 1.12:
    - función compute_annual_energy
    - errores: el caudal de diseño se recalculaba en cada escenario y la Config A no dividía el mínimo técnico por unidades.
    - assert sobre la potencia máxima
    - tabla de 5 escenarios
    - validación de D4: +1.4% y −1.8%, como cota superior y no material
    - ranking de materialidad: el caudal ecológico primero, con la fuente más débil.
 - 1.13:
    - exportación del CSV con 6 columnas y control de ida y vuelta
    - bug de isin (valores contra índice)
    - tres gráficos guardados con savefig
 - Bug del loop: for q in pisaba la serie q y aparecía con Run All
 - Entorno: el kernel crasheó de nuevo por abrir VS Code fuera del prompt activado.
 - Versiones fijadas en environment.yml.

- Aprendí:
 - análisis de sensibilidad y materialidad
 - qué queda fijo y qué cambia en cada escenario
 - funciones, parámetros por defecto y alcance de variables
 - assert
 - “la energía del caudal medio no es igual a la energía media”
 - el control contra el límite físico (87,6 GWh)
 - datos crudos contra procesados
 - reproducibilidad

- No entendí:
    - Nada pendiente

- Ayuda de IA:
 - el esqueleto de la función;
 - el bloque corregido de la validación de D4;
 - la estructura de la tabla;
 - el arreglo del loop
 - checklists de contenido

## 2026-10-21 · 5 h
- Hice:
 - learning log del 20/10
 - README completo (corregido en dos rondas)
 - puerta aprobada con correcciones
 - justificación y limitación del Q30 en la D8
 - auditoría completa del repo
 - corrección de la leyenda del gráfico
 - cierre del pendiente de la D7
 - informe de cierre

- Aprendí:
 - qué va en un README y qué no (integridad)
 - links e imágenes en Markdown
 - la diferencia entre una elección convencional y una optimizada (Q30)
 - que un archivo puede cambiar solo por los finales de línea

- No entendí:
 - Nada pendiente

- Ayuda de IA:
 - revisión del README
 - auditoría independiente (recálculo del CSV y revisión de los gráficos)
 - redacción del informe de cierre
 - Guía de estudio en PDF (la escribió la IA completa).

 ## 2026-10-22 · 7 h
- Hice:
 - Analisis de persistencia de años secos (1.14).
 - Organizacion de años por semestre (1.15).
 - Completar D10.
 - Correcciones y completar README.
 - Correcciones y completar Learning Log.
 - Análisis de Población mezcla (1.16).
 - Análisis de Estacionariedad (1.17).
 - Se obtuvo respuesta de Dr. Catalini y su colocación de la cita en D1


- Aprendí:
 - Importancia de organizacion de datos por semestre, por su implicancia financiera.
 - Análisis de población mezcla (1.16) mediante coeficiente de pearson y spearman
 - Análisis de estacionariedad mediante prueba de Mann-Kendall

- No entendí:
 - Nada pendiente

- Ayuda de IA:
 - Ayuda en la celda de código 1.15 y la línea que calcula la participación del caudal oct-mar (72,7%).
 - Explicación de los conceptos de la 1.14 (autocorrelación, test de rachas) con fuentes. 
 - Verificación independiente de los resultados de la 1.14 y de la 1.15.
 - Búsqueda y verificación de fuentes: IRENA (2012), Operis y Wall Street Playbook.
 - Edición directa de la IA en el repo: borró los caracteres invisibles de DECISIONS.md y un archivo de bloqueo de git.
 - Actualización del informe de cierre y de la guía en PDF.
 - Esqueletos de código de la 1.16 y la 1.17, los conceptos con fuentes (Helsel) y verificacion de control con calculos independientes.
 - Borrado de los caracteres invisibles del notebook.
