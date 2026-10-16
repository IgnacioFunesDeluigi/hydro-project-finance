# Decisions

## D1 · 2026-10-15 · Research question
Decision: size debt at P90 energy from daily streamflow; thesis storm methods move to a v2 flood module.
Why: design storms drive flood peaks, not annual energy yield.
Source: project roadmap, section 1.

## D2 · 2026-10-15 · Python version
Decision: dedicated conda environment "hydro" from conda-forge, Python pinned to 3.13.
Why: pandas supports Python 3.14 only since 2.3.3; 3.13 has a longer track record and lowers the risk that later libraries (e.g. PyTorch in phase 6) lack 3.14 builds.
Source: https://pandas.pydata.org/pandas-docs/version/2.3/whatsnew/v2.3.3.html (EST; PyTorch 3.14 support: VERIFICAR)

## D3 · 2026-10-15 · Chosen stream gauge
Decision: The chosen stream gauge to analyze the historical data was "Guido" located in Mendoza, Argentina.
Why: "Guido" stream gauge has the following record: 1956-07-01 to 2026-06-30 (about 70 years), includes the 2010s-2020s drought, needed to test H1.
"Guido" stream gauge is located in the lower part of the upper basin, 15 kilometers upstream from the "Potrerillos" reservoir (OFICIAL, Latin America Water Fund Partnership). The reservoir does not regulate the flow measured at the station. 
Pensado (2016) and Salomón et al. (2005), as cited in "Análisis de Factibilidad de Fondo de Agua en la Cuenca del Río Mendoza", p. 13 states that river discharge depends primarily on seasonal snowmelt, while the remainder comes from glacial melt and rainfall, the latter being a more significant contributor during dry years. There is no information regarding the existence of water intakes upstream, for a high-mountain watershed it is reasonable to assume that these are minor (EST). 
Considering that there are two types of data: consolidated data (data that has already been processed and reviewed by the agency), and real-time data (raw sensor records, unvalidated), it was decided to work with the consolidated data.
Source: https://snih.hidricosargentina.gob.ar/ ; https://www.mendoza.gov.ar/wp-content/uploads/sites/15/2022/12/FONDO-de-Agua-de-la-Cuenca-del-Rio-Mendoza-FINAL-OK.pdf