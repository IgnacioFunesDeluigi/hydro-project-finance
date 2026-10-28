# Decisions

## D1 · 2026-10-15 · Research question

**Decision:** size debt at P90 energy from daily streamflow; thesis storm methods move to a v2 flood module.

**Why:** design storms drive flood peaks, not annual energy yield.

**Source:**
 - Project roadmap, section 1.
 - C. G. Catalini, personal communication, October 22, 2026: written authorization to use and cite his design-storm methodologies and neural-network-generated series in the flood-risk module (v2).

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
 - Sensitivity done in section 1.12: at 20%, P50 −10.8% and P90 −19.4%; at 30%, P50 −25.5% and P90 −41.0%. It is the most material assumption (VERIFICAR)

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
 - The head is back-calculated from the power equation [P = ρ · g · Q · H_n · η]. The Head is a design parameter for a hypothetical power plant. The relevant limitation is that, with a low head and high flow rate, the cost per installed kW is higher (IRENA 2012, section 4.1) : a factor that is factored into the CAPEX for stage 2.
 - Comparative CAPEX without a source: in other words, It is assumed that a single Kaplan unit has lower CAPEX than two units (A or C); no reliable source was found (VERIFICAR).
 - Q30 was not optimized. ESHA (2004, section 3.6) identifies the design flow through an optimization over a range of flows; this requires CAPEX and will be tested in the financial model (stage 2)

**Sources:**
 - ESHA (2004), Guide on How to Develop a Small Hydropower Plant: Section 1.3 (head classification) and Table 3-2, p. 62 (technical minimum). https://energycommunityplatform.eu/wp-content/uploads/2022/06/Merged-Guide-Develop-a-Small-Hydropower-Plant.pdf
 - USBR (2005): efficiency ~90%. https://www.usbr.gov/power/edu/pamphlet.pdf
 - NTUA: Power equation and net head. https://www.itia.ntua.gr/el/getfile/2050/7/documents/06_SmallHydroSupplementary.pdf
 - Tsuanyo et al. (2023), Table 2: head ranges. https://tethys-engineering.pnnl.gov/publications/design-models-small-run-river-hydropower-plants-review
 - IRENA (2012), Renewable Energy Technologies: Cost Analysis Series, Hydropower, section 4.1, fig. 4.3. https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2012/RE_Technologies_Cost_Analysis-HYDROPOWER.pdf
 - (EST) for η and the configuration.
 - (VERIFICAR) for CAPEX.

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
 - The method treats years as independent. The data show that low years come in dry streaks (runs test: 24 runs vs 35.5 expected, z = −2.79; lag-1 autocorrelation 0.64, section 1.14). The risk of several bad years in a row is not captured by a one-year P90. Persistence confirmed in 1.14; its effect on debt (H1) and covenant risk (H3) is tested in stages 2–3. (updated 2026-10-22)
 - With 69 values, the P90 depends on a small number of low years.
 - The results inherit the assumptions of D4, D7 and D8, and the simplification of constant flow during each day (section 1.10).

**Sources:**
 - Penn State EME 810, 8.4 Exceedance Probabilities: P50, P75, P90: https://courses.ems.psu.edu/eme810/node/630
 - EIA Glossary, "Capacity factor": https://www.eia.gov/tools/glossary/index.php?id=C
 - Own analysis: notebooks/01_hydrology.ipynb, section 1.11 and section 1.14
 - Method: https://pandas.pydata.org/docs/reference/api/pandas.Series.quantile.html
 - NIST/SEMATECH e-Handbook 1.3.5.12, Autocorrelation. https://www.itl.nist.gov/div898/handbook/eda/section3/eda35c.htm
 - NIST/SEMATECH e-Handbook 1.3.5.13, Runs Test. https://www.itl.nist.gov/div898/handbook/eda/section3/eda35d.htm
 - (EST)

## D10 · 2026-10-22 · Semiannual periods for the energy series [EST]

 **Decision:**
 - It was decided to generate another .CSV file ['data/processed/semiannual_energy.csv'] in which the years are organized by semester. Specifically, the semesters spanning October–March and April–September are selected. These semesters are labeled according to the hydrological year in which they end; additionally, the energy generated during each half of the year is broken down.

**Why:**
 - The financial model is structured on a semi-annual basis, as this is the typical frequency for debt service in project finance. In other words, the data is organized in this stage to facilitate its interpretation in subsequent phases.
 - The semesters: October - March and April - September are chosen to ensure consistency with the previous decision (D6): this allows the thaw periods to be contained entirely within a single semester, thereby preventing them from being split across the transition between semesters.
 - The cutoff separates the high-generation season (Oct–Mar, accounting for 65.7% of the energy and 72.7% of the flow) from the low-generation season. The P50/P90 values for each six-month period are 38.0/29.8 GWh (Oct–Mar) and 18.7/13.6 GWh (Apr–Sep).

 **Alternative considered:**
 - The alternative considered was to use calendar semesters (Jan–Jun / Jul–Dec): Calendar semesters split the thaw period in two, and each semester combines months of high and low generation. This is why it was ultimately discarded to ensure consistency with the aforementioned D6.

 **Limitations:**
 - This setup exports the base scenario; it does not export alternative scenarios such as eco20, eco30, or Config A.
 - The contribution from October to March is flattened due to the design flow limit. From October to March, an average of 65.7% of the energy is generated, yet 72.7% of the river's flow occurs during this period.
 - The actual debt payment dates are set in stage 2, which means they might not align with the end of the semesters. This will need to be verified at a later stage.

**Sources:**
 - D6: 'Determining the Hydrological Year'
 - https://www.operis.com/loan-life-cover-ratio-explanation/
 - https://www.wallstreetplaybook.org/blog/project-finance-modeling-guide
 - Notebook section 1.15.
 
## D11 · 2026-10-24 · Structuring of the semestral P90 [EST]

**Decision:**
 - It was decided (A) to divide the annual P90 value into semesters as follows: P90 (annual) * average profile (for the semester). This results in the following:
    - Oct to Mar = 45.0 GWh * 65.7% = 29.6 GWh
    - Apr to Sep = 45.0 GWh * 34.3% = 15.4 GWh
Thus, the sum totals 45.0 GWh.
 - Alternative (B) is discarded as a base case and remains as a sensitivity analysis case for the subsequent steps. The risk of a dry semester occurring is not entirely eliminated, as it will be accounted for in the Monte Carlo simulation in stage 3, using actual years and semesters.
 - The participation rate is the year-by-year average from October to March (65.7%), rather than the ratio of the sums (65.05%).
 - The recent case (2010–2025) uses the P90 value for the 2010–2025 period (42.24 GWh) along with the recent profile (67.75%), ensuring that both the level and the seasonality correspond to the same period.

**Why:**
 - P90 is annual, and banks typically measure the DSCR over a 12-month period (Forvis Mazars, https://financialmodelling.forvismazars.com/resources/debt-service-coverage-ratio-dscr/). The bank aims to secure the P90 year, and, as determined in the previous stage, the annual value is 45.0 GWh.

 - The analysis of participation is based on annual averages (rather than the ratio of the sums) because:
   - It ensures consistency with the results from stage 1 (hydrology).
   - It allows each year to carry equal weight in determining the percentage of participation for the two periods: Oct–Mar and Apr–Sep. If these percentages were calculated as the ratio of the sums, wetter years would have a disproportionately greater influence on the resulting percentages.

 - It has been decided to calculate a distinct P90 value for the recent period (2010–2025), as this timeframe coincides with the recent "megadrought." This period is atypical compared to preceding years, and it is worth treating it separately, given that its P90 value is even lower.

**Alternative considered:**
 - Another alternative was considered in which the P90 value for each six-month period is calculated separately (Alternative B):
    - Oct to Mar = 29.8 GWh
    - Apr to Sep = 13.6 GWh
The sum of both is 43.4 GWh. As can be seen, this total is lower than the 45.0 GWh previously determined; this is because this alternative combines the dry six-month period of one year with that of another, effectively constructing a 43.4 GWh year (a more conservative scenario than the annual P90). In other words, it is a doubly conservative scenario, which is why the decision was made to discard this alternative as a base case.

**Limitations:**
 - Alternative (A) does not account for the risk of an actual dry semester. However, this will be covered by the Monte Carlo simulation in later stages.
 - The case of the recent decade: 2010–2025 is a unique one, as it constitutes a 16 year "megadrought."

**Sources:**
 - Forvis Mazars, https://financialmodelling.forvismazars.com/resources/debt-service-coverage-ratio-dscr/
 - EST

## D12 · 2026-10-24 · Operating assumptions [EST]

**Decision:**
 - Availability factor = 92% 
 - Energy price = 65	USD/MWh 
 - Price escalation =	0	%/yr 
 - Fixed O&M (% of CAPEX) =	3	%/yr
 - Variable O&M = 0	USD/MWh
 - O&M escalation =	2	%/yr

**Why:**
 - Availability factor = 92% ; 95% as a technical baseline (accounting for preventive maintenance and mechanical repairs), minus 3% due to operational shutdowns forced by water turbidity. Dr. Catalini confirmed that there are occasional shutdowns due to turbidity, but the 3% reduction was not a figure provided by him; rather, it was an assumption.
 - Energy price = 65	USD/MWh ; Recent MATER contracts (for eolic and solar energy) indicate a value in the range of 60 to 70 USD/MWh. A figure of 65 USD/MWh is taken as an estimate, assuming that the same prices apply to hydroelectric energy.The ±10% sensitivity in step 2.9 covers that uncertainty.
 - Price escalation =	0	%/yr ; In the absence of public disclosure of adjustment clauses in private contracts. It maintains a nominal flat rate throughout the term of the contract.
 - Fixed O&M (% of CAPEX) =	0.03	%/yr ; The IRENA paper states that O&M costs generally range from 1% to 6% of total CAPEX for small hydroelectric plants. A figure of 3% is assumed as a central value within the 1–6% range.
 - Variable O&M = 0	USD/MWh ; Run-of-river power plants have a marginal variable cost that is practically zero (as they require no fuel or direct inputs per MWh). All operational and preventive expenses are covered under fixed O&M costs.
 - O&M escalation =	2 %/yr ; It corresponds to the official long-term inflation target of the United States Federal Reserve (US CPI/PCE) for financial models structured in nominal dollars.

**Limitations:**
 - Availability factor: Both the 95% technical baseline and the 3% reduction for turbidity-related stoppages are purely our own estimates. Tested with a sensitivity (e.g., 88%) in step 2.9
 - Energy price = 65	USD/MWh ; The sources consulted establish a price range of 60 to 70 USD/MWh for wind and solar energy sources. It is assumed that this same range applies to hydroelectric energy.
 - Fixed O&M (% of CAPEX) = 3%/yr; The IRENA paper states that for small hydroelectric power plants, these percentages can be even higher. In this case, it has been decided to use a central value within the 1–6% range.

**Sources:**
 - Availability factor: Own criteria ; Personal communication with Dr. Catalini [EST]
 - Energy price: https://www.energiaestrategica.com/energiaestrategica/en/notes/del-renovar-al-mater-cuanto-cuestan-las-renovables-en-argentina-y-que-esperar-a-futuro [EST]
 - Price escalation: Own criteria [EST]
 - Fixed O&M (% of CAPEX): IRENA: RENEWABLE ENERGY TECHNOLOGIES: COST ANALYSIS SERIES [2012] https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2012/RE_Technologies_Cost_Analysis-HYDROPOWER.pdf. Added to this,IRENA RENEWABLE POWER GENERATION COSTS IN 2024 https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf stablishes that the average O&M is “slightly less than 2%” and also “smaller projects approach the higher end of the range”
 - Variable O&M: Own criteria [EST]
 - O&M escalation: Statement on Longer-Run Goals and Monetary Policy Strategy https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf [EST]


## D13 · 2026-10-24 · Construction assumptions [EST]

**Decision:**
 - Construction period = 24 months
 - CAPEX = 3300 USD/kW. 
 - Contingency % = 0% 
 - Development costs = 0
 - CAPEX disbursement curve	= 15% / 35% / 35% / 15%	 per period
 
**Why:**
 - Construction period =	24 months ; The construction period for a hydroelectric power plant depends essentially on its specific details; therefore, there is no fixed, predetermined timeframe. In the case of a small hydroelectric power plant, an execution period of 24 months is assumed.
 - CAPEX = 3300 USD/kW ; IRENA 2024 data (Table 6.3, small-scale hydropower of 10 MW or less, in 2024 dollars): “Other South America” for 2010–2017 shows 3,307. Brazil shows 2,698 for 2010–2017 and 2,534 for 2018–2024. The global total for the 0–50 MW range (Table 6.2) shows an average of 2,067, with a range of 1,011 to 4,407. 
 The regional data point closest to Argentina is used, and a value higher than that of Brazil is selected because: 
   1) The 26.9 m head falls right at the threshold below 25–30 m where, according to IRENA (2012), economies of scale related to hydraulic head are "modest." 
   2) Construction works and equipment in Argentina are subject to import costs. 
   3) A single turbine does not allow for the dilution of fixed costs.
 10,000 kW × 3,300 = USD 33 million in 2024 dollars. The ±15% CAPEX sensitivity from step 2.9 covers a range of 2,800 to 3,800.
 The IRENA costs are in 2024 dollars. Since the model uses nominal dollars, the CAPEX for each half year on the "Construction" sheet is adjusted from 2024 to the date of expenditure, using the 2% rate already established.
 - Contingency % = 0% : IRENA’s cost figures reflect the actual costs of projects that have already been built. Any cost overruns that occurred are already factored into the average; therefore, adding an additional contingency would result in double-counting. 
In any case, a bank would still require a contingency in the construction budget, but in this instance, it will be covered by the sensitivity analysis.
 - Development costs = 0 : IRENA defines its total installed cost as “including fixed financing costs,” and also clarifies that “owner costs” encompass project development. Therefore, development costs are already included in the 3,300 figure.
 - CAPEX disbursement curve	= 15% / 35% / 35% / 15%	 per period ; It follows the typical “S-curve”: low expenditure at the beginning (mobilization, engineering) and at the end (installation, commissioning), with high expenditure in the middle. For small run-of-river power plants, civil works account for 50% of the cost, mechanical components for 30%, and electrical components for 20%. Civil works are carried out during the first three semesters, while equipment is paid for upon delivery between the second and fourth semesters.

**Limitations:**
 - Construction period =	24 months ; A 6 month delay is a potential sensitivity.
 - CAPEX : Since there was no fixed, clear value for CAPEX, an estimate had to be made. Furthermore, the amount had to be expressed in 2024 USD and escalated to nominal USD of each disbursement period at 2%/yr.
 - Contingency %: The risk of cost overruns is addressed through a sensitivity analysis using a +15% CAPEX scenario.
 - CAPEX disbursement curve	= 15% / 35% / 35% / 15%	 per period: It does not correspond to any actual, existing curve; rather, it is an estimate based on the typical curves associated with this type of project.

**Sources:**
 - Construction period: Own criteria,IRENA: RENEWABLE ENERGY TECHNOLOGIES: COST ANALYSIS SERIES https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2012/RE_Technologies_Cost_Analysis-HYDROPOWER.pdf 
 - CAPEX: Own criteria, IRENA: RENEWABLE POWER GENERATION COSTS IN 2024, table 6.3. https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf
 - Contingency %: Own criteria, IRENA: RENEWABLE POWER GENERATION COSTS IN 2024, chapter 6. https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf
 - Development costs: IRENA: RENEWABLE POWER GENERATION COSTS IN 2024, chapter 6. https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf
 - CAPEX disbursement curve: Own criteria, IRENA: RENEWABLE POWER GENERATION COSTS IN 2024, table 6.1. https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf
 

## D14 · 2026-10-26 · Debt term sheet [EST]

**Decision:**
 - Debt tenor	= 12 years
 - Debt interest rate =	9	%/yr
 - Semiannual interest rate	= 4.5	%/semester
 - Target DSCR (P90) = 1.35 x
 - Lock-up DSCR covenant = 1.2 x
 - Default DSCR covenant = 1.1 x
 - Maximum gearing = 70 %
 - DSRA (months of debt service) = 6 months
 - Upfront fee = 1.5 %
 - Commitment fee = 0.5 %
 
**Why:**
 - Debt tenor	= 12 years ; Reference case: BID invest provided a loan to Central Puerto for La Castellana wind farm (99 MW) with a total tenor of 15 years (holding a contract with CAMMESA, under RenovAr program, a more robust counterparty than a private entity under the MATER framework). For this reason, it was decided to select a 12 year repayment period (14 years including construction phase).
 - Debt interest rate =	9	%/yr ; Reference case: In November 2025, Genneia (largest renewable energy generator in Argentina), issued an 8 year corporate bond for 400 million, with 7.75 coupon and 8% yield. In this case, it was decided to select a debt interest rate slightly higher because this SPV is a new company, with a single asset, no previous projects and a private buyer in MATER framework. Added to this, country risk rose to 675 points on 10/19/2026, the highest level of the year.
 - Semiannual interest rate	= 4.5	%/semester ; When a loan involves semiannual payments, splitting the debt interest rate in half is the standard practice.
 - Target DSCR (P90) = 1.35 x ; Forvis Mazars suggest a multiple of around 1.3x for infrastructure with contracted revenue, and a multiplier between 1.2x and 1.35x when there is a solid buyer. It was decided to choose the upper limit of this range because the buyer is a private entity and the project is located in Argentina (country risk). Added to this, The projections are made based on the P90 scenario, therefore there is no need to go any higher.
 - Lock-up DSCR covenant = 1.2x & Default DSCR covenant = 1.1x ; According to Forvis Mazars, the lock up threshold is set below the target DSCR, and the default threshold is set even lower. Their example uses 1.1x for default. It was decided to pick a multiple of 1.2x because it falls between the two.
 - Maximum gearing = 70 % ; Wall Street Prep uses 75% in their example. According to argentine risk, it was decided to pick a maximum gearing of 70%.
 - DSRA (months of debt service) = 6 months ; This is the standard, cited by CFI and BIWS.
 - Upfront fee = 1.5 % & Commitment fee = 0.5 % ; IDCOL (Bangladesh´s state owned infrastructure bank) sets its rates for foreign currency loans as 1%-2% of the loan amount, and a commitment fee of 0.50%-0.75%. Even though this is not an Argentina bank, it serves as reference.

**Limitations:**
 - Debt tenor	= 12 years ; The term of the power purchase agreement must be at least as long as the term of the debt.
 - Debt interest rate =	9	%/yr ; The rate is obtained from a corporate bond issued by a large company, not from a project finance loan to an SPV. 

**Sources:**
 - Debt tenor : https://idbinvest.org/es/medios-y-prensa/bid-invest-financia-el-proyecto-eolico-la-castellana-para-diversificar-la-matriz
 - Debt interest rate: https://www.lanacion.com.ar/economia/genneia-coloco-una-on-por-us400-millones-nid20112025/ ; https://www.noticiasnqn.com.ar/noticias/2026/10/19/357254-el-riesgo-pais-subio-a-675-puntos-y-alcanzo-su-nivel-mas-alto-de-2026
 - Semiannual interest rate	: Own criteria
 - Target DSCR (P90) : https://financialmodelling.forvismazars.com/resources/debt-service-coverage-ratio-dscr/
 - Lock-up DSCR covenant & Default DSCR covenant : https://financialmodelling.forvismazars.com//resources/debt-service-coverage-ratio-dscr/
 - Maximum gearing: https://www.wallstreetprep.com/knowledge/debt-sizing-in-project-finance/
 - DSRA : CFI & BIWS: https://corporatefinanceinstitute.com/resources/commercial-lending/debt-service-reserve-account-dsra/ ; https://breakingintowallstreet.com/kb/project-finance/debt-service-reserve-account/
 - Upfront fee & Commitment fee : https://idcol.org/home/fees 

## D15 · 2026-10-26 · Tax and project life [EST]

**Decision:**
 - Income tax rate = 35% 
 - Share of civil works in CAPEX = 50 %
 - Fiscal life of equipment = 10 years
 - Fiscal life of civil works = 50 years
 - Tax loss carryforwards = 5 years
 - Project life / water concession = 30 years
 
**Why:**
 - Income tax rate = 35% ; According to PwC, a 35% rate applies to taxable income exceeding ARS 1,335 million (based on 2026 figures). With the wholesale dollar exchange rate at ARS 1,513 (Rava, Oct 14, 2026), that threshold is approximately USD 0.88 million. The power plant generates revenues of about 45 GWh × 92% × 65 USD/MWh ≈ USD 2.7 million per year, with O&M costs of around USD 1.0 million. Therefore the SPV falls in the top bracket once equipment depreciation ends; a flat 35% is used as a simple, slightly conservative assumption.
 - Share of civil works in CAPEX = 50% ; Table 6.1 from IRENA 2024 indicates that for small run of river power plants, 50% for civil works, 30% for mechanical components, and 20% electrical. Mechanical and electrical components together constitute the equipment.
 - Fiscal life of civil works = 50 years & Fiscal life of equipment = 10 years ; PWC Deductions establishes that buildings are depreciated at 2% per year (50 years lifespan), and machinery and equipment have a standard useful life of 10 years.
 - Tax loss carryforwards = 5 years ; According to PWC, Loss carrybacks are not permitted, the carryforward period is 5 years.
 - Project life / water concession = 30 years ; IRENA 2024 uses a conservative economic life of 30 years for hydroelectric plants. In July 2026, the province of Mendoza launched the bidding process for the Los Nihuiles complex with a 30 year concession. 

**Limitations:**
 - Income tax rate ; The scale is in Argentinian pesos, and is indexed annually ; The minimum tax and other levies (gross receipts taxes, municipal fees) are not modeled.
 - Project life / water concession ; The concession for the river is not defined, the 30 year term is derived from an analogous case
 - During the first 10 years, the depreciation of equipment generates tax losses, and a portion of these may expire before they can be used


**Sources:**
 - Income tax rate:  https://taxsummaries.pwc.com/argentina/corporate/taxes-on-corporate-income ; https://www.rava.com/cotizaciones/historico/dolar-mayorista/2026/10/14/
 - Share of civil works in CAPEX: https://www.irena.org/Publications/2025/Jun/Renewable-Power-Generation-Costs-in-2024
 - Fiscal life of civil works & Fiscal life of equipment: https://taxsummaries.pwc.com/argentina/corporate/deductions
 - Tax loss carryforwards: https://taxsummaries.pwc.com/argentina/corporate/deductions 
 - Project life / water concession: https://www.irena.org/Publications/2025/Jun/Renewable-Power-Generation-Costs-in-2024 ; https://www.diariouno.com.ar/sociedad/mendoza-abrio-el-proceso-licitar-los-nihuiles-y-buscar-un-nuevo-operador-30-anos-n1579308

## D16 · 2026-10-26 · Timeline conventions [EST]

**Decision:**
 - Semesters aligned with the hydrological year
 - Financial close (FC) date: 1 October 2027
 - Debt tenor and project life calculated from the COD
 - Flags evaluated based on the period start date
 - Escalation base: 1 July of CAPEX base year
 - 70 columns ; Minimum number of periods : 60 operation periods + 4 construction periods
 
**Why:**
 - Data_Energy data is organized by hydrological semester (D10, D11), so the model's time periods must align with the data. The Data_Energy semesters represent periods of high and low production; therefore, analysis by semester is the most appropriate approach.
 - The financial close date must fall on October 1st or April 1st so that the six-month periods align with D10. Furthermore, setting it for October 2027 allows for about 12 months to secure permits and financing.
 - Debt tenor and project life are calculated from the Commercial Operation Date (COD), as this marks the point at which the power plant has been constructed and is operational, the precise moment when the construction phase ends and the commercial operation phase begins.
 - FC, COD and debt maturity always fall on a period start date (1 October or 1 April), so evaluating flags on the start date assigns each period to exactly one phase 
 - IRENA provides an annual average for 2024, and the midpoint of the year serves as its representative point.
 - 70 columns are used in timeline because 6 spare periods allow Project life to increase up to 33 years without adding columns

**Limitations:**
 - The construction check assumes that the construction period is a multiple of 6 months.
 - The closing date is tentative.
 - If Project Life exceeds 33 years, there will be a shortage of columns, so they would need to be added manually.

**Sources:**
 - https://courses.renewablesvaluationinstitute.com/pages/academy/how-to-use-flags-in-financial-models
 - https://support.microsoft.com/en-us/office/edate-function-3c920eb2-6e66-44e7-a1f5-753ae47ee4f5
 - https://support.microsoft.com/en-us/office/eomonth-function-7314ffa1-2bc9-4005-9d66-f49db127d628

## D17 · 2026-10-27 · Construction funding, fees and IDC [EST]

**Decision:**
 - Model units in USD
 - Type of disbursement: pro rata
 - Provisional debt = maximum gearing rate x construction cost
 - Commissions and IDC paid in equity
 - IDC and commitment fee calculated based on the average balance for the half year
 - Upfront fee paid during the first six months (first semester) of construction
 
**Why:**
 - Pro rata: Yescombe states that banks accept either an "equity first" or a "pro rata" approach. The pro rata method represents a middle point for the sponsor’s IRR and it adjusts automatically when the debt amount changes
 - Paying with equity avoids circularity in v1
 - Average balance: disbursements occur throughout the semester; calculating based on the opening balance would leave the first semester without interest
 - Upfront fee at closing: charged a single time, upon signing

**Limitations:**
 - With commissions and IDC paid via equity, the effective gearing drops to 65%; in practice, IDC and fees are often capitalized into the loan or funded with a debt/equity mix (BIWS); revisited in step 2.6
 - The average balance is an approximation: it assumes that disbursements are distributed evenly throughout the semester
 - The debt is provisional until section 2.6

**Sources:**
 - Yescombe 13.3: https://www.globalspec.com/reference/38628/203279/13-3-drawdown-of-debt-and-equity
 - BIWS IDC: https://breakingintowallstreet.com/kb/project-finance/interest-during-construction-idc/
 - D14 for commissions fees

## D18 · 2026-10-27 · Operating cash flow [EST]

**Decision:**
 - Case selector
 - Fixed O&M based on the 2024 CAPEX, escalated from 01/07/2024
 - Price escalated from the COD
 - Pre-tax CFADS = EBITDA.
 
**Why:**
 - Case selector: Allows switching between different scenarios: P50, P90 and recent historical series.
 - Fixed O&M based on the 2024 CAPEX, escalated from 01/07/2024: IRENA reference capital and operating costs in a specific base year (2024). Taking July 1st represents the midpoint of that base year. Fixed O&M is a % of the 2024 USD CAPEX, so it is in 2024 USD and must be escalated from the same base date.
 - Price escalated from the COD: The contract price applies from COD, so its escalation starts there (own criteria). With Price escalation = 0% (D12), this has no effect in the base case
 - Pre-tax CFADS = EBITDA: BIWS defines CFADS as EBITDA – cash taxes +/- change in working capital – maintenance CapEx. Taxes are added in step 2.5, and working capital and maintenance CapEx are not modeled in v1, so pre-tax CFADS equals EBITDA

**Limitations:**
 - There is no consideration of working capital or a reserve for major maintenance.
 - Fixed O&M is constant in real terms for 30 years (only escalated by inflation); plant ageing is not modeled.

**Sources:**
 - D11
 - https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_2025.pdf
 - https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals.pdf
 - D12
 - https://breakingintowallstreet.com/kb/project-finance/cash-flow-available-for-debt-service-cfads/

## D19 · 2026-10-27 · Income tax [EST]

**Decision:**
 - Depreciable base = CAPEX + contingency + development costs. IDC and loan fees are deducted when accrued, not capitalized
 - Straight line depreciation from COD
 - Tax calculated per semester
 - Losses with a 10 semester expiration period, applied on a FIFO basis (first in first out, MIN method)
 - Interest expense in operations = 0 (placeholder) until step 2.6
 
**Why:**
 - LIG art. 85 a) allows deducting interest and loan fees in the fiscal year,  Decree 862/2019 art. 207 excludes interest from the cost of depreciable assets. The 30% limit of art. 85 applies only to debt with related parties; the senior loan is from an unrelated lender
 - Loss expiry is material: about USD 5.4M of losses expire unused in the P90 case, so it cannot be simplified
 - FIFO: the oldest losses are used first, and the balance never exceeds those generated within the window

**Limitations:**
 - Interpretation of the tax rules is my own and has not been reviewed by a tax advisor
 - If sponsors fund part of the equity as shareholder loans, the 30% limit of art. 85 would apply
 - 40% of the civil base is not depreciated within 30 years
 - The tax is calculated by hydrological half year, not by fiscal year, and without advance payments
 - There is no minimum tax or gross receipts tax (this was already included in D15).

**Sources:**
 - Law (t.o. 2019): https://servicios.infoleg.gob.ar/infolegInternet/anexos/330000-334999/332890/texact.htm
 - Decree 862/2019: https://www.argentina.gob.ar/normativa/nacional/decreto-862-2019-332991/actualizacion
 - BIWS CFADS (cash taxes). https://breakingintowallstreet.com/kb/project-finance/cash-flow-available-for-debt-service-cfads/
 - PwC Deductions (losses already included in D15)
 - Microsoft Support, SUMIFS. https://support.microsoft.com/es-ES/Excel/functions/sumifs-function

## D20 · 2026-10-28 · Debt sizing and sculpting [EST]

**Decision:**
 - Debt = MIN(capacity based on DSCR; maximum gearing × total uses)
 - Debt capacity = PV of CFADS / 1.35, discounted at the semi-annual debt rate
 - Semiannual sculpting.
 - Circularity: [debt -> IDC/fees/interest -> tax -> CFADS]. This circularity was solved by copying and pasting the debt and k values as static values, with checks in place
 
**Why:**
 - A debt is worth the same as the PV of its payments, discounted at its own rate
 - Gearing is measured against total uses, as this is how the bank calculates it: debt / (debt + equity)
 - Copying and pasting avoids triggering Excel’s iterative calculation [circularity], which can hide errors
 
**Results:**
 - Debt of 8,064,963, as dictated by the DSCR, the gearing limit is 25,624,682
 - Debt covers 22% of total uses (36.61 M)

**Limitations:**
 - During the first 5 dry semesters, debt service is less than the interest (resulting in negative principal), causing the balance to grow. An alternative approach involves dry semesters consisting only of interest payments, with the DSCR measured over a 12 month period, based on a debt amount of 8,063,244 (−0.02%). This is deferred to version 2 (v2)
 - Values must be updated manually, whenever an assumption changes (Wehn switching the case selector: 1,2,3)
 - There is no DSRA yet (step 2.7)

**Sources:**
 - https://financialmodelling.forvismazars.com/resources/debt-service-coverage-ratio-dscr/
 - https://breakingintowallstreet.com/kb/project-finance/interest-during-construction-idc/
 - exercises/01_sculpting_3_periods.xlsx

## D21 · 2026-10-28 · DSRA and cash waterfall [EST]

**Decision:**
 - DSRA target = 6/12 of the next 12 months debt service, funded with equity at COD
 - Lock-up and default, measured using the DSCR for the last 12 months.
 - All available cash is distributed. A negative distribution represents an equity injection

**Why:**
 - DSRA target on the next 12 months: a target equal to the next semester's debt service would swing between about 896k and 264k, requiring a top-up of about 620k in dry semesters with only about 95k of cash available. Using the next 12 months smooths the target and keeps the input in months
 - 12-month DSCR for covenants, as stated in D11 (Forvis Mazars)
 - Full distribution with negative distributions as equity injections: sponsors are the only party that would fund an operating shortfall.

**Results:**
 - DSRA initial funding = 588,265
 - Total distributions = 20,257,172
 - No lock-up or default events.

**Limitations:**
 - The four dry semesters from 2056 to 2059 show a negative CFADS, as O&M costs increase by 2% while prices remain flat (0% escalation). It is required to review this in section 2.9, using a sensitivity analysis for price escalation.
 - DSRA does not generate interest
 - A default is merely a flag, its consequences are not modeled

**Sources:**
 - BIWS DSRA: https://breakingintowallstreet.com/kb/project-finance/debt-service-reserve-account/
 - https://financialmodelling.forvismazars.com/resources/debt-service-coverage-ratio-dscr/
