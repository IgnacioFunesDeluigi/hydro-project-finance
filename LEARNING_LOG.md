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

## 2026-10-22 - 2026-10-23 · 5 h
- Hice:
  - Estructura del repo: model/, exercises/, docs/model_book.md, y ~$* en .gitignore.
  - Workbook hydro_pf_model_v1.xlsx con 13 hojas (Cover → Checks).
  - Ejercicio 01_sculpting_3_periods.xlsx. El límite de gearing es el que manda (19.6 < 21.01): ajuste con el factor k, saldo final 0 y DSCR resultante 1.394.

- Aprendí:
  - SPV y deuda non-recourse.
  - CFADS y DSCR, distinguiendo el target de dimensionamiento del covenant.
  - Sculpting. Debt capacity = VP(CFADS/DSCR) a la tasa de la deuda.
  - Deuda = mín(capacidad por DSCR, límite de gearing). Cuando manda el gearing, DSCR = target / k.
  - LLCR, DSRA, cascada de flujos, lock-up y default, IDC y circularidad, Sources & Uses.
  - Estándar FAST: inputs en azul, tiempo en columnas, sin valores fijos dentro de las fórmulas, porcentajes como decimales.

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Recopilacion de conceptos y respuesta de dudas respecto a conceptos financieros
  - Recopilacion de fuentes verificadas
  - Guía de conceptos y cheat sheet en Drive, y la hoja de ruta 2.1–2.10.


## 2026-10-24 · 5 h
- Hice:
  - Data_Energy:
    - P50 = 57.07 GWh, P90 = 45.02 GWh, P90 reciente (2010–2025) = 42.24 GWh.
    - Participación Oct–Mar: 65.73% en el período completo y 67.75% en el reciente.
    - Tabla de casos semestrales (Oct–Mar / Abr–Sep, GWh): P50 37.51/19.56, P90 29.59/15.43, Recent 28.62/13.62.
  - D11: P90 semestral con el método A (P90 anual × perfil estacional medio, calculado como promedio de ratios).
  - D12:
    - Availability factor 92%, Energy price 65 USD/MWh, Price escalation 0.
    - Fixed O&M 3% del CAPEX, Variable O&M 0, O&M escalation 2% (meta de la Fed).
  - D13:
    - CAPEX 3,300 USD/kW (IRENA 2024, tabla 6.3).
    - Development costs 0 y Contingency 0, porque el costo de IRENA ya los incluye.
    - CAPEX base year 2024.
    - CAPEX disbursement 15/35/35/15, con CONTROL en la fila siguiente.
    - Construction period 24 meses.

- Aprendí:
  - Los percentiles no se suman: P90 anual ≠ suma de los P90 semestrales.
  - Promedio de ratios contra ratio de sumas.
  - El DSCR se mide sobre 12 meses (Forvis Mazars).
  - Valores nominales contra reales, y escalación desde un año base.
  - Costo real de obra (as-built) contra costo presupuestado: sumar contingencia a un costo real es contarla dos veces.

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Recopilacion de conceptos y respuesta de dudas respecto a conceptos financieros
  - Recopilacion de fuentes verificadas

## 2026-10-26 · 5 h
- Hice:
  - D14:
    - Debt tenor 12 años (BID Invest).
    - Debt interest rate 9% (comparable: Genneia) y Semiannual interest rate = tasa / 2.
    - Grace period 0.
    - Target DSCR 1.35, Lock-up DSCR covenant 1.20, Default DSCR covenant 1.10 (Forvis Mazars).
    - Maximum gearing 70% y DSRA de 6 meses.
    - Upfront fee 1.5% y Commitment fee 0.5% (IDCOL).
  - D15:
    - Income tax rate 35%.
    - Share of civil works in CAPEX 50%.
    - Vidas fiscales: 50 años la obra civil y 10 para los equipos.
    - Tax loss carryforwards 5 años.
    - Project life 30 años (IRENA y el caso de Los Nihuiles).
  - Timeline y D16
  - Inputs reorganizado en 6 bloques.

- Aprendí:
  - Cupón contra rendimiento (yield) de un bono, y riesgo país (675 bps).
  - Tasa nominal / 2 contra tasa efectiva.
  - Covenants de lock-up y default.
  - Impuesto a las ganancias progresivo en pesos
  - Amortización fiscal por tipo de activo y quebrantos impositivos.
  - La concesión del agua limita la vida del proyecto.

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Recopilacion de conceptos y respuesta de dudas respecto a conceptos financieros
  - Recopilacion de fuentes verificadas

## 2026-10-27 · 6 h
- Hice:
  - 2.2 Timeline (completado la noche del 26/10):
    - Fechas clave: FC, COD, inicio de repago, vencimiento de la deuda y fin de la operación.
    - 70 semestres alineados al año hidrológico, banderas de construcción, operación y repago, Years from base.
    - Checks y D16.
  - 2.3 Construction:
    - CAPEX nominal escalado (35,72 M) e INDICE en la curva de desembolso.
    - Funding pro rata y corkscrew de la deuda durante la obra.
    - Comisiones e IDC sobre el saldo promedio.
    - Sources & Uses y D17.
  - 2.4 Operations:
    - Selector de caso, energía, precio escalado desde el COD.
    - O&M escalado desde 2024, EBITDA y D18.
  - 2.5 Tax:
    - Amortización de obra civil y equipos.
    - Quebrantos con vencimiento a 10 semestres (método MIN y SUMAR.SI.CONJUNTO), impuesto y CFADS.
    - Investigación de la LIG (art. 85) y del Decreto 862/2019 (art. 207): IDC y comisiones se deducen al devengarse, no se activan.
    - D19.

- Aprendí:
  - FECHA.MES / FIN.MES, banderas 1/0 y fechas evaluadas al inicio del período.
  - Nominal contra real en el CAPEX.
  - Órdenes de desembolso: equity first, pro rata, debt first (Yescombe).
  - Upfront fee, commitment fee, IDC y circularidad.
  - Sources & Uses.
  - EBITDA y CFADS (BIWS).
  - Amortización fiscal, quebrantos y FIFO.
  - IAS 23 (contable) contra la ley argentina (fiscal).
  - Una misma columna = un mismo semestre en todas las hojas.

- Errores:
  - Ambigüedad día/mes en las fechas (usar el formato 2027-10-01).
  - Referencias a filas de Inputs que se corrieron (CAPEX escalation en lugar de Price escalation).
  - Checks que daban 0 por casualidad (bases civil y de equipos invertidas).
  - Fórmulas corregidas en una sola columna.
  - Valores escritos a mano donde iba un link (selector de caso).

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Recopilación de conceptos y respuesta de dudas respecto a conceptos financieros
  - Recopilación de fuentes verificadas
  - Investigación de la normativa fiscal argentina (LIG y Decreto 862/2019)
  - Verificación de valores por cálculos independientes

## 2026-10-28 · 5 h
- Hice:
  - Debt:
    - Capacidad por DSCR (VP del CFADS / 1,35) y límite de gearing.
    - Deuda de 8,06 M, la manda el DSCR.
    - Tabla de deuda, circularidad cerrada con valores pegados (deuda y k) y D20.
  - Cashflow:
    - DSRA (6/12 de los próximos 12 meses).
    - Cascada, DSCR a 12 meses, lock-up y default, dividendos (las distribuciones negativas son aportes) y D21.
  - Ratios y Returns: DSCR y LLCR (1,35), project IRR −0,67%, equity IRR −2,02% y D22.

- Aprendí:
  - Una deuda vale el VP de sus pagos a su propia tasa.
  - Circularidad y su cierre copiando y pegando valores.
  - DSRA, cascada de caja, covenants de lock-up y default.
  - LLCR
  - TIR semestral anualizada.
  - Apalancamiento negativo.
  - AGGREGATE cuando falta MINIFS (Excel 2013).

- Hallazgos:
  - Principal negativo en los semestres secos (v2).
  - CFADS negativo en 2056–2059.
  - Proyecto marginal con P90.

- Errores:
  - Referencias de fila corridas al insertar filas.
  - Totales en lugar de valores por semestre (el Debt service).
  - Fórmulas que miraban hacia adelante (DSCR a 12 meses).
  - Fórmula del lock-up invertida.

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Recopilacion de conceptos y respuesta de dudas respecto a conceptos financieros
  - Recopilacion de fuentes verificadas
  - Verificacion de valores por calculos independientes

## 2026-10-29 · 5 h
- Hice:
  - Modo de dimensionamiento (1 y 2) y cronograma de P90 pegado.
  - Caso e-flow 20%.
  - Tabla de 12 sensibilidades.
  - Respuesta principal: −32,6% de deuda con P90 contra P50.
  - D23.
  - Hoja Checks (23 checks, status y Info).
  - Aportes de los sponsors durante el lock-up y D24.

- Aprendí:
  - Caso del banco (P90) contra caso del sponsor (P50 con la deuda fija).
  - Sensibilidades de a un supuesto por vez.
  - Ranking de supuestos: el caudal ecológico pesa más que cualquier supuesto financiero.
  - Un check que falla puede estar mostrando una situación real (default con e-flow 20%), no un error.

- Errores:
  - Fijacion de celdas faltante en la referencia al modo.
  - Porcentaje cargado como entero (escalamiento de 2 en lugar de 0,02).
  - Pasar al modo 2 sin repegar la deuda de P90.

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Recopilacion de conceptos y respuesta de dudas respecto a conceptos financieros
  - Recopilacion de fuentes verificadas
  - Verificacion de valores por calculos independientes

## 2026-10-30 · 5 h
- Hice:
  - Model book completo, con estructura ampliada.
  - Caso disponibilidad 88% (deuda 7,43 M).
  - Corrección de los labels I-02 e I-03.
  - Reconstrucción de la fórmula del sculpting (criterio de la puerta de la etapa 2)

- Aprendí:
  - Qué es un model book y para qué lo usa un revisor.
  - Cómo se documenta un modelo: run procedure, test log, issue log.
  - La reconstrucción del sculpting: DSCR resultante = objetivo / k y por qué LLCR = DSCR.

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Recopilacion de conceptos y respuesta de dudas respecto a conceptos financieros
  - Recopilacion de fuentes verificadas
  - Verificacion de valores por calculos independientes
  - Revision y edicion del model book

## 2026-10-31 a 2026-11-01 · 5 h
- Hice:
  - Paso 3.0 de correcciones antes del Monte Carlo (D25-D28).
  - Semestres secos solo intereses: ventana de 12 meses, descuento anual 1 + 2r, checks de primer y último semestre (cierra I-01).
  - Piso de deuda y guardas para deuda cero; test T-05 con precio 0 (pasa).
  - Plazo de contrato de 20 años y precio poscontrato: opción B como base y C (spot) como sensibilidad.
  - LCOE, tasa hurdle (Damodaran H1) y tarifa requerida por rondas manuales de Goal Seek: 100.77 y 159.71 USD/MWh.
  - Nueva corrida de la tabla de sensibilidades y tablas 2 y 3 (respuesta principal a la tarifa requerida).

- Aprendí:
  - Por qué el banco no acepta amortización negativa y cómo se evita con semestres secos solo intereses.
  - El LCOE como precio de equilibrio y la diferencia con la tarifa que exige el sponsor.
  - Apalancamiento operativo: a mayor precio, la reducción de deuda P90 vs P50 tiende al 21%.
  - Goal Seek tiene una tolerancia de 0.001; se resuelve con una celda auxiliar multiplicada por 1.000.000.

- Errores:
  - Pegar la deuda con el selector equivocado y sobrescribir la fórmula de C17 con un valor.
  - Olvidar repegar el cronograma P90 y copiar resultados antes de que Excel recalculara.
  - Tasa hurdle cargada como 0.188 en lugar de 0.1888; checks sin ABS en la hoja Checks.

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Investigación de fuentes (MATER, precio spot, Damodaran, Bodmer).
  - Diseño propuesto de fórmulas (ventana de 12 meses, descuento 1 + 2r, guardas de deuda cero).
  - Verificación independiente de todos los valores con una réplica en Python.
  - Correcciones de DECISIONS.md (D25-D28) y edición del model book y del README.

## 2026-11-01 a 2026-11-04 · 3 h
- Hice:
  - Paso 3.0b (D29): las ventanas de 12 meses octubre-septiembre no estaban controladas (1.278 en la primera fecha de septiembre y 1.186 al vencimiento, debajo del lock-up de 1.20).
  - Sculpting semestral con traspaso estacional constante c (69,000 USD): todos los DSCR a 12 meses en 1.35 salvo la primera fecha de test, sin lock-up.
  - Checks nuevos: DSCR a 12 meses = objetivo / k, c pegado = c calculado, principal >= 0.
  - Sensibilidades nuevas de tasa ±0.5 pt y nueva corrida de las tablas 1 y 2 (tarifas 100.77 y 159.90 USD/MWh; respuesta principal 32.65%).

- Aprendí:
  - Cómo funcionan las ventanas móviles de 12 meses del covenant y por qué cada pago entra en dos ventanas.
  - Si todas las ventanas valen el objetivo, el servicio de deuda solo puede ser CFADS / objetivo ± una constante.
  - Redondear c no cambia las ventanas y hace converger el bucle de pegado más rápido.
  - El costo de la opción A: DSCR semestral menor a 1 en los últimos semestres secos, cubierto por la DSRA.
  - La reducción porcentual se calcula siempre sobre la deuda del caso base.

- Errores:
  - Fórmula de la fila 12 pegada una columna corrida y bloque de c una fila más arriba.
  - Checks nuevos escritos en la hoja Checks en lugar de Debt (pisaron el vínculo al check del LLCR).
  - Celda auxiliar de Goal Seek con la fórmula de 2.A al correr 2.B (dio 97.34).
  - Reducción por tasa +1 pt dividida por la deuda nueva (4.8% en lugar de 4.63%).
  - Filas de sensibilidad sin pegar como valores y modelo dejado con la deuda del último escenario.

- No entendí:
  - Nada pendiente

- Ayuda de IA:
  - Diagnóstico de las ventanas de septiembre, derivación de la opción A y propuesta de fórmulas y checks.
  - Verificación independiente de todos los valores con una réplica en Python.
  - Redacción de D29 y actualización del model book, del README y de este registro.

## 2026-11-05 a 2026-11-07 · 9 h (estimado, confirmar)
_Borrador escrito por la IA a partir de la sesión; pendiente de revisión de Ignacio._
- Hice:
  - Paso 3.1: conceptos de Monte Carlo, bootstrap, bootstrap por bloques circular, error estándar y semillas.
  - D30: predicciones preregistradas para H3, métrica por métrica, antes de simular.
  - D31: simulación principal con la deuda P90 fija y su cronograma (opción A).
  - Paso 3.2: `src/cashflow.py` con `read_row`, `load_constants` y `run_trajectory` (energía, ingresos, EBITDA, impuestos con quebrantos FIFO, CFADS, DSRA, DSCR a 12 meses, lock-up, default, distribuciones y equity IRR). Coincide con el Excel del caso base semestre por semestre.
  - Paso 3.3: D32 (alcance de la conciliación), tres fixtures del Excel y `tests/test_reconciliation.py` con pytest; el T-08 corrido en v1.2 (24 lock-up y 24 default).
  - Paso 3.4: autocorrelación real contra 0,64^k, Politis-White (L = 8, D33).
- Aprendí:
  - Por qué el Monte Carlo sortea futuros en lugar de elegir una trayectoria representativa (el banco mira la cola, no el promedio).
  - Por qué L = 1 rompe la persistencia y L = 12 repite la historia; cómo elegir L con la banda de 1,96/√n y con Politis-White.
  - Separar lo que cambia con la hidrología (ingresos, impuestos, CFADS, DSCR) de lo que no (CAPEX, intereses, servicio de deuda con la deuda fija).
  - Por qué un covenant default puede dispararlo un solo año y la DSRA no lo evita (la DSRA no entra en el CFADS).
  - Escribir la predicción antes del resultado (preregistro) y fecharla con un commit.
- Errores:
  - Sangría: código fuera del bucle o de la función; `np.min(a, b)` en lugar de `min(a, b)`; usar `opening` de otro bucle; `[t]` de más o de menos; `^` en lugar de `**`.
  - Fin de línea CRLF en varios archivos (resuelto con `core.autocrlf input`).
  - Test escrito en `tests/fixtures/` y una comprobación comparando contra la fila equivocada.
- No entendí:
  - Al principio, la diferencia entre deuda fija y redimensionada (D31) y el alcance de la conciliación (D32); lo entendí con la explicación en palabras simples.
- Ayuda de IA:
  - Explicaciones de conceptos con fuentes; esqueletos de código de cada bloque de `run_trajectory`; el test de conciliación (agregué 4 comprobaciones); detección de bugs; cálculo de Politis-White y verificación independiente de todos los resultados contra el Excel; borrado de caracteres invisibles en `DECISIONS.md`.

## 2026-11-08 a 2026-11-09 · 7 h (estimado, confirmar)
_Borrador escrito por la IA a partir de la sesión; pendiente de revisión de Ignacio._
- Hice:
  - Muestreador `block_bootstrap` (bloques circulares con `%`) en `src/bootstrap.py` y primera trayectoria: 1969 dispara el default.
  - `summarize_trajectory` y `simulate`; D34 (definición de las métricas).
  - Simulaciones a 65 y a 100,77 USD/MWh; prueba sin impuesto (ablación) que mide el timing impositivo.
  - Período reciente 2010-2025 con L = 4 y L = 8 (D35): cero defaults y más lock-ups.
  - Serie semestral de e-flow 20% exportada del notebook 01; fixture `eco20_sized.xlsx` y simulación con su propia deuda (D36).
- Aprendí:
  - El caso P90 es pesimista en promedio pero no en los extremos: supone 45 GWh todos los años y nunca un 1969.
  - El apalancamiento operativo (1,85): cada 1% de energía que falta saca casi 2% de CFADS.
  - Un año húmedo puede provocar un default años después: el sculpting supone cuándo se usan los quebrantos.
  - Números aleatorios comunes: comparar escenarios con la misma semilla.
  - La falta de un año extremo en 16 años no prueba que no exista (62% de no verlo aunque el clima no cambie).
  - Un caudal ecológico fijo agranda la dispersión relativa de los años secos.
- Errores:
  - Pegar código de prueba dentro de `src/`; claves de diccionario que no existían; reutilizar nombres de variables (`sims`, `c`) que pisaron resultados.
  - Simular e-flow 20% con la tabla de energía del caso base.
- No entendí:
  - El mecanismo del timing impositivo y el del perfil estacional; los entendí con la tabla semestre por semestre.
- Ayuda de IA:
  - Esqueletos de `summarize_trajectory` y `simulate`; diagnóstico del timing impositivo y prueba del perfil estacional (D36); verificación independiente de cada resultado; pasos para exportar la serie de e-flow 20%.

## 2026-11-10 a 2026-11-11 · 11 h (estimado, confirmar)
_Borrador escrito por la IA a partir de la sesión; pendiente de revisión de Ignacio._
- Hice:
  - Tabla de resultados por escenario (`data/processed/montecarlo_results.csv`).
  - H3 con L = 1, 2, 4, 6, 8, 10 y 12 (D37): rechazada para el banco, válida para el sponsor.
  - Convergencia en N y en semillas; N = 10.000 (D38).
  - H1: racha seca más larga contra año más seco, tabla de 2 × 2 y Spearman (D39): parcialmente rechazada.
  - Simulación con la deuda dimensionada a P50 (D40): respuesta central completa (94% contra 24%).
  - Tres gráficos en `docs/figures/`, README de la etapa 3.
- Aprendí:
  - Leer una simulación contra su error estándar: con N = 1.000 la mayoría de las "tendencias" eran ruido.
  - La diferencia entre el promedio y la dispersión (`.mean()` contra `.std()`).
  - El desvío entre semillas tiene que ser del tamaño del error estándar; si es mucho mayor, hay un bug.
  - Apalancamiento operativo contra apalancamiento financiero.
  - Una hipótesis que sale falsa, con el mecanismo entendido y predicho por escrito, es un resultado.
- Errores:
  - Una semilla aleatoria sin fijar en la prueba de semillas; el error estándar de una celda anterior usado en otra; notebooks guardados sin correr de arriba abajo.
  - Tablas de Markdown con encabezados que no coincidían con las filas; números truncados en lugar de redondeados.
- No entendí:
  - Al principio, el error en la definición de la DSRA agotada (D34) y cómo se plantea H1; los entendí con la explicación en palabras simples.
- Ayuda de IA:
  - La definición inicial de las métricas de DSRA y sponsors la propuso la IA y tenía un error: contaba semestres posteriores al préstamo. La IA lo detectó en una revisión semestre por semestre y se corrigió en D34.
  - Esqueletos de las pruebas de convergencia, de `longest_run` y del gráfico 1 y su estilo; revisión de los gráficos; arreglos menores del README; actualización del model book (versión 1.3) y borrador de este registro.
