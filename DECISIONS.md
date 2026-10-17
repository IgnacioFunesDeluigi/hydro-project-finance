# Decisions

## D1 · 2026-10-15 · Research question

**Decision:** size debt at P90 energy from daily streamflow; thesis storm methods move to a v2 flood module.

**Why:** design storms drive flood peaks, not annual energy yield.

**Source:** project roadmap, section 1.

## D2 · 2026-10-15 · Python version

**Decision:** dedicated conda environment "hydro" from conda-forge, Python pinned to 3.13.

**Why:** pandas supports Python 3.14 only since 2.3.3; 3.13 has a longer track record and lowers the risk that later libraries (e.g. PyTorch in phase 6) lack 3.14 builds.

**Source:** https://pandas.pydata.org/pandas-docs/version/2.3/whatsnew/v2.3.3.html (EST; PyTorch 3.14 support: VERIFICAR)

## D3 · 2026-10-15 · Chosen stream gauge

**Decision:** the chosen stream gauge to analyze the historical data was "Guido" located in Mendoza, Argentina.

**Why:** "Guido" stream gauge has the following record: 1956-07-01 to 2026-06-30 (about 70 years), includes the 2010s-2020s drought, needed to test H1.
"Guido" stream gauge is located in the lower part of the upper basin, 15 kilometers upstream from the "Potrerillos" reservoir (OFICIAL, Latin America Water Fund Partnership). The reservoir does not regulate the flow measured at the station. 
Pensado (2016) and Salomón et al. (2005), as cited in "Análisis de Factibilidad de Fondo de Agua en la Cuenca del Río Mendoza", p. 13 states that river discharge depends primarily on seasonal snowmelt, while the remainder comes from glacial melt and rainfall, the latter being a more significant contributor during dry years. There is no information regarding the existence of water intakes upstream, for a high-mountain watershed it is reasonable to assume that these are minor (EST). 
Considering that there are two types of data: consolidated data (data that has already been processed and reviewed by the agency), and real-time data (raw sensor records, unvalidated), it was decided to work with the consolidated data.

**Source:**
- https://snih.hidricosargentina.gob.ar/ 
- https://www.mendoza.gov.ar/wp-content/uploads/sites/15/2022/12/FONDO-de-Agua-de-la-Cuenca-del-Rio-Mendoza-FINAL-OK.pdf

## D4 · 2026-10-16 · Interpolation of the missing dates

**Decision:** there are 103 missing dates, and they are grouped in 3 big clear groups (1962-09-01 to 1962-09-30 with 30 missing dates ; 1976-06-22 to 1976-07-31 with 40 missing dates ; 1985-06-01 to 1985-06-30 with 30 missing dates), the other 3 dates are scattered and they do not constitute a problem. With this in mind, it was decided to interpolate the flow ('q_m3s') values related with the missing dates, using the 'time' method, which interpolates the value associated with the index based on the time spans between the measured data points. 

**Why:** it was decided to interpolate these values and not to discard the missing data groups because this would skew hypothesis H1. Also, the missing data groups are related with winter season: period of low, stable and predictable flow. Added to this, the measured values before and after the missing groups are similar. [To be validated by comparing P50/P90 annual energy with and without the 5 affected years.].

**Source:** 
- Own analysis.
- Notebooks/01_hydrology.ipynb, section 1.2 (gap table: long gaps fall in low-flow winter months).
- Method: https://pandas.pydata.org/docs/reference/api/pandas.Series.interpolate.html (EST)

## D5 · 2026-10-16 · Criterion for determining a dry year

**Decision:**
- A year is considered “dry” if its mean annual flow is below the median of the mean annual flows.
- The median is calculated based on 69 full years (1957–2025), excluding 1956 and 2026 as they are incomplete.
- The resulting threshold is 40.8 m³/s.
- Updated: superseded by D6, analysis now uses hydrological years (Oct-Sep)

**Why:**
- The median divides the dataset into two equal halves and is not skewed by extreme years, such as 1983 or 1987, whereas the mean would be.
- It is a simple, reproducible criterion that is easy to explain to a committee.
- It is useful for identifying sequences of consecutive dry years, which is what H1 tests.
- Alternative considered: the DGI classifies years into categories (dry, poor, normal, wet) based on the percentage of the historical mean runoff. This was discarded for the time being because, for H1, a binary division (dry or not dry) is sufficient.

**Limitations:**
- This is a criterion based on the historical record itself: “dry” means “drier than half of the years on record for this river”. It is neither a physical nor an official threshold.
- It includes years that contain interpolated days (D4).

**Sources:**
- Own analysis, notebooks/01_hydrology.ipynb, section 1.5.
- Method: https://pandas.pydata.org/docs/reference/api/pandas.Series.median.html
- Alternative: https://www.irrigacion.gov.ar/web/wp-content/uploads/2024/06/DGI_INFORME_ANUAL_21_22.pdf
- Own analysis, notebooks/01_hydrology.ipynb, section 1.6.
- (EST)

## D6 · 2026-10-17 · Determining the Hydrological Year

**Decision:**
 - D5 used calendar years provisionally; calendar years split each snowmelt season (Dec-Jan) in two. This requires us to adopt a different organizational approach in which the years begin with the period of lowest flow, so that a complete snowmelt season falls within the same year (July through October ≈ 20–27 m³/s; January ≈ 98 m³/s).
 - As explained above, river flow is primarily influenced by snowmelt, so the snowmelt flow from a single season is spread across two different years (since the division occurs between December and January, a period of high flow).
 - Therefore, the decision has been made to process the data by dividing it into hydrological years running from October to September.  
 - Each hydrological year is labeled by the year in which it ends (hydrological year 1957 = 1956-10-01 to 1957-09-30)

**Why:**
 - The Mendoza General Irrigation Department (the provincial water resource authority for the river in question) has explicitly adopted this hydrological year as the official standard (OFICIAL). Every October, the DGI prepares a runoff forecast for the coming season.
 - Looking ahead to the next stages of the project, the plant’s annual energy output will be calculated by adding up the days in each year. If the year ends in the middle of summer, the snowmelt from a single season is split between two different years. One year would appear to be dry and the other wet, even though the river has not changed. That distortion would be directly reflected in the P50 and P90 analyses.

 **Alternative considered:**
 - The historical data set from the Argentine National Water Information System begins in July 1956 and ends in June 2026. This time frame is another option and could be fully applied to the analysis. However, it was decided to rule it out since it would represent a personal, unofficial decision. It is worth noting that if this alternative had been chosen, 70 years of data would have been available instead of 69; however, given the large number of years for which data was available, it was decided to discard this alternative.

 **Limitations:**
 - 69 complete hydrological years (1957-2025, labeled by end year), one fewer than the July-June alternative (70), since 3 months are lost at the beginning and 9 months at the end of the historical time series of measurements

**Sources:**
 - Own analysis: notebooks/01_hydrology.ipynb (monthly mean flows).
 - https://www.irrigacion.gov.ar/web/wp-content/uploads/2024/06/DGI_INFORME_ANUAL_21_22.pdf (OFICIAL)
 - (EST)
 