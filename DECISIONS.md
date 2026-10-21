# Decisions

## D1 · 2026-10-15 · Research question

**Decision:** size debt at P90 energy from daily streamflow; thesis storm methods move to a v2 flood module.

**Why:** design storms drive flood peaks, not annual energy yield.

**Source:** project roadmap, section 1.

## D2 · 2026-10-15 · Python version

**Decision:** dedicated conda environment "hydro" from conda-forge, Python pinned to 3.13. Versions pinned in environment.yml on 2026-10-20 (python 3.13.16, pandas 3.0.6, numpy 2.5.4, matplotlib 3.11.2, openpyxl 3.1.5, jupyterlab 4.6.4)

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

**Why:** it was decided to interpolate these values and not to discard the missing data groups because this would skew hypothesis H1. Also, the missing data groups are related with winter season: period of low, stable and predictable flow. Added to this, the measured values before and after the missing groups are similar. Results [in section 1.12]:
 - ΔP50 = +1.4% and ΔP90 = −1.8%, based on a 64-year time series.
 - This is an upper bound on the interpolation effect, because measured days are also excluded, which changes the sample.
 - It is non-material parameter compared to the ecological flow (−19% at the P90).
 - Physical argument: 103 days (0.4% of the record), in winter, with low and stable flow.
 - Conclusion: The interpolation remains unchanged.


**Source:** 
- Own analysis.
- Notebooks/01_hydrology.ipynb, section 1.2 (gap table: long gaps fall in low-flow winter months).
- Method: https://pandas.pydata.org/docs/reference/api/pandas.Series.interpolate.html (EST)
- Notebooks/01_hydrology.ipynb, section 1.12 (validation).

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
 
 ## D7 · 2026-10-18 · Ecological flow

**Decision:**
 - The ecological flow is constant and equal to 4.4 m³/s, which is 10% of the average daily flow over the 69 complete hydrological years (44.0 m³/s).
 - Using the ecological flow: the river flow is reduced day by day: q_available = (q_hy − q_ec).clip(lower=0). Negative results are ignored because they are meaningless.
 - The design flow and all energy calculations use q_available, not the river flow.

**Why:**
 - No biological studies of the site were found, nor were there any regulations from Mendoza or the DGI that establish a numerical value. This is why the Tennant (1975) method is used.
 - 10% of the average annual flow corresponds to the “Poor or Minimum” threshold in Table 1. Although a flow corresponding to 30% is also defined as the “fair or degrading” level for the high-flow season, it was decided to use the minimum of 10% for the calculations.

 **Alternative considered:**
 - Tennant with seasonal values: a higher percentage during the peak season, which on the Mendoza River runs from October to March due to the reversal of seasons. This was ruled out at this stage for the sake of simplicity. However, it will be considered for the model's sensitivity analysis.

 **Limitations:**
 - 10% is Tennant's minimum: it is the least restrictive option for the plant and, therefore, optimistic in terms of energy. A regulator might require more.
 - The method was developed using rivers in the Northern Hemisphere (Montana) and is not specifically calibrated for a snowmelt-fed Andean river.
 - A constant value ignores seasonality.
 - [PENDING]: P50/P90 energy sensitivity with an ecological flow of 20% and 30% of the mean annual flow

**Sources:**
 - Tennant, D. L. (1975), Instream Flow Regimens for Fish, Wildlife, Recreation and Related Environmental Resources, USFWS, Table 1: https://files.dep.state.pa.us/Water/BSDW/Public_Water_Supply_Permits/TennantMethodPaper_1975.pdf
 - Own analysis: notebooks/01_hydrology.ipynb, section 1.8.
 - Tags: (EST) for the method and (VERIFICAR) for the local regulatory requirement.

  ## D8 · 2026-10-19 · Head, efficiency and turbine configuration

**Decision:**
 - The project is based on the assumption of an installed capacity of 10 MW 
 - A constant efficiency value of η = 0.88 is assumed. For now, we will not consider that this value changes with the flow rate entering the turbine.
 - The design flow rate is set at 43.0 m3/s. The methods used to arrive at this value are detailed in the notebook.
 - Using the power equation, the required net head is calculated to be 26.9 meters.
 - The configuration of the base hydroelectric power plant is “Config. B”: 1 Kaplan turbine with a capacity of 43.0 m3/s, with a technical minimum flow rate of 15% (6.45 m3/s).

**Why:**
 - 26.9 m is considered a low head according to ESHA [(European Small Hydropower Association, 2004), section 1.3] (<30 m) and falls within the range for a Kaplan turbine, but at the lower end of the range for a Francis turbine.
 - Days below the minimum technical flow:

 | Config | Complete period | Dry years |
| :--- | :---: | ---: |
| A (2×Francis) | 3.5% | 7.1% |
| B (1×Kaplan) | 0.05% | 0.1% |
| C (2×Kaplan) | 0.0% | 0.0% |

 - Configuration B is virtually the same as C in terms of days lost and is simpler from an operational standpoint: a single machine.

 - The design flow is Q30 of the available flow, a conventional starting point within the typical Q30–Q40 range for run-of-river plants
 
 **Alternative considered:**
 - C (2×Kaplan): redundancy and better efficiency at partial load. Ruled out for the base case for simplicity; remains as an alternative.
 - A (2×Francis): the worst in terms of lost days. This is reflected in the sensitivity analysis in 1.12 (P50/P90 of A versus B).

 **Limitations:**
 - η is constant : the model does not account for the drop in efficiency at partial load, so it is optimistic scenario for B.
 - No redundancy: A failure or maintenance means zero power generation. Pending: Availability assumption.
 - The head is back-calculated from the power equation [P = ρ · g · Q · H_n · η]. It has not been measured on site (VERIFICAR: DEM or topographic survey).
 - Comparative CAPEX without a source: in other words, It is assumed that a single Kaplan unit has lower CAPEX than two units (A or C); no reliable source was found (VERIFICAR).
 - Q30 was not optimized. ESHA (2004, section 3.6) identifies the design flow through an optimization over a range of flows; this requires CAPEX and will be tested in the financial model (stage 2)

**Sources:**
 - ESHA (2004), Guide on How to Develop a Small Hydropower Plant: Section 1.3 (head classification) and Table 3-2, p. 62 (technical minimum). https://energycommunityplatform.eu/wp-content/uploads/2022/06/Merged-Guide-Develop-a-Small-Hydropower-Plant.pdf
 - USBR (2005): efficiency ~90%. https://www.usbr.gov/power/edu/pamphlet.pdf
 - NTUA: Power equation and net head. https://www.itia.ntua.gr/el/getfile/2050/7/documents/06_SmallHydroSupplementary.pdf
 - Tsuanyo et al. (2023), Table 2: head ranges. https://tethys-engineering.pnnl.gov/publications/design-models-small-run-river-hydropower-plants-review
 - (EST) for η and the configuration.
 - (VERIFICAR) for the head and CAPEX.

## D9 · 2026-10-19 · Method for P50 and P90 of annual energy

**Decision:**
 - Annual energy is calculated by adding the daily energy of each complete hydrological year (69 years, 1957-2025, D6).
 - P50 and P90 are the empirical percentiles of these 69 annual values: P50 = quantile(0.50), P90 = quantile(0.10), using pandas (linear interpolation).
 - Results: mean 56.7 GWh, P50 57.1 GWh, P90 45.0 GWh, P90/P50 = 0.79. Plant factor: 65.1% (P50) and 51.4% (P90).

**Why:**
 - The record is long (69 complete years) and includes the main dry streaks, so the empirical distribution already contains the real variability of the river.
 - The method is simple, reproducible and easy to explain to a committee. It does not need to assume a shape for the distribution.
 - P50 and P90 are the values banks use to judge if a project can pay its debt; the P90 is used to size the debt (D1).

**Alternative considered:**
 - Fitting a statistical distribution (for example, a normal distribution) to the 69 annual values and reading the P90 from it. Not used for now because it adds an assumption about the shape of the distribution that is not needed with 69 years of data. It can be used later as a check.

**Limitations:**
 - The method treats years as independent. The data show that low years come in dry streaks (6 of the 7 years below the P90 are inside streaks). The risk of several bad years in a row is not captured by a one-year P90 (H1, to be tested in the financial stage).
 - With 69 values, the P90 depends on a small number of low years.
 - The results inherit the assumptions of D4, D7 and D8, and the simplification of constant flow during each day (section 1.10).

**Sources:**
 - Penn State EME 810, 8.4 Exceedance Probabilities: P50, P75, P90: https://courses.ems.psu.edu/eme810/node/630
 - EIA Glossary, "Capacity factor": https://www.eia.gov/tools/glossary/index.php?id=C
 - Own analysis: notebooks/01_hydrology.ipynb, section 1.11.
 - Method: https://pandas.pydata.org/docs/reference/api/pandas.Series.quantile.html
 - (EST)