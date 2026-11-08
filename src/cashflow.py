import pandas as pd
import numpy as np
import numpy_financial as npf

def read_row(path, sheet, label):

    # Return the 70 per-period values of the row whose label (column A) matches

    df = pd.read_excel(path, sheet_name=sheet, header=None)
    labels = df[0].astype(str).str.strip()
    row = df[labels == label]
    return row.iloc[0, 3:].to_numpy(dtype=float)

def load_constants(path):
    constants = {
        "debt_service": read_row(path, "Debt", "Debt service"),
        "construction_flag": read_row(path, "Timeline", "Construction flag"),
        "operations_flag": read_row(path, "Timeline", "Operations flag"),
        "repayment_flag": read_row(path, "Timeline", "Repayment flag"),
        "semester": read_row(path, "Timeline", "Semester"),
        "energy_price": read_row(path, "Operations", "Energy price"),
        "price_escalation_index": read_row(path, "Operations", "Price escalation index"),
        "fixed_om": read_row(path, "Operations", "Fixed O&M (semiannual)"),
        "total_tax_depreciation": read_row(path, "Tax", "Total tax depreciation"),
        "financing_costs": read_row(path, "Tax", "Total deductible financing costs"),
        "dsra_target": read_row(path, "Cashflow", "DSRA target"),
        "initial_funding": read_row(path, "Cashflow", "+ Initial funding"),
        "equity_contribution": read_row(path, "Construction", "Total equity contribution"),
        "tax_rate" : 0.35,
        "lockup": 1.2,
        "default": 1.1,
        "availability": 0.92,
        "loss_life": 10,
    }
    return constants



def run_trajectory(energy_gwh, c):
    # 1. Place the 60 operating semesters on the 70-period axis
    energy_full = np.zeros(70)
    energy_full[c["operations_flag"] == 1] = energy_gwh

    # 2. Revenue and EBITDA (model book 6.5)
    net_mwh = energy_full * c["availability"] * 1000                              # GWh -> MWh, after availability
    revenue = net_mwh * c["energy_price"] * c["price_escalation_index"]           # net energy x price (x escalation index)
    ebitda =  revenue - c["fixed_om"]                                             # revenue - operating costs


    # 3. Tax with FIFO tax losses (model book 6.6, Tax rows 22-33)
    taxable = ebitda - c["total_tax_depreciation"] - c["financing_costs"]
    generated = np.maximum(0, -taxable)       # semester by semester MAX(0, -x)

    closing = np.zeros(70)
    used = np.zeros(70)
    expired = np.zeros(70)
    for t in range(70):                       # t = 0, 1, ..., 69
        opening = closing[t - 1] if t > 0 else 0.0
        used[t] = min(opening, max(0, taxable[t]))
        before_expiry = opening + generated[t] - used[t]
        valid = generated[max(0, t - c["loss_life"] + 1): t + 1].sum()
        closing[t] = min(before_expiry, valid)
        expired[t] = before_expiry - closing[t]

    tax = (np.maximum(0,taxable) - used) * c["tax_rate"]  # (Positive earning - loss) * 35% tax rate
    cfads = ebitda - tax

    # 4. Cash waterfall: DSRA, 12-month DSCR, covenants, distributions (model book 6.8)
    ds = c["debt_service"]
    cash_after_ds = cfads - ds
    topup = np.zeros(70)
    withdrawal = np.zeros(70)
    release = np.zeros(70)
    dsra = np.zeros(70)
    dscr_12m = np.zeros(70)
    lockup = np.zeros(70)
    default = np.zeros(70)
    distributions = np.zeros(70)
    retained = np.zeros(70)

    for t in range(70):
        # DSRA corkscrew
        dsra_open = dsra[t - 1] if t > 0 else 0.0
        if c["repayment_flag"][t] == 1:
            topup[t] = min(max(0,(c["dsra_target"][t] - dsra_open)),max(0,cash_after_ds[t]))
        withdrawal[t] = min(dsra_open,max(0,-cash_after_ds[t]))
        release[t] = max(0,dsra_open+c["initial_funding"][t]+topup[t]-withdrawal[t]-c["dsra_target"][t])
        dsra[t] = dsra_open + c["initial_funding"][t] + topup[t] - withdrawal[t] - release[t]
        cash_available = cash_after_ds[t] - topup[t] + withdrawal[t] + release[t]

        # 12-month DSCR and covenants
        ds_window = ds[t] + (ds[t - 1] if t > 0 else 0.0)
        if c["repayment_flag"][t] == 1 and ds_window > 0:
            dscr_12m[t] = (cfads[t-1] + cfads[t]) / (c["debt_service"][t-1] + c["debt_service"][t])
            if dscr_12m[t] < c["lockup"] :
                lockup[t] = 1 
            else:
                lockup[t] = 0 
            if dscr_12m[t] < c["default"] :
                default[t] = 1 
            else:
                default[t] = 0 

        # Retained cash corkscrew
        retained_open = retained[t-1] if t > 0 else 0.0
        if lockup[t] == 1:
            distributions[t] = min(0,retained_open+cash_available)
        else:
            distributions[t] = retained_open+cash_available
        retained[t] = retained_open + cash_available - distributions[t]

    equity_cf = distributions - c["equity_contribution"]
    equity_irr = ( 1 + npf.irr(equity_cf))**2 -1

    return { "net_mwh": net_mwh, "revenue": revenue, "ebitda": ebitda,"used":used, "expired":expired, "tax": tax, "cfads":cfads, "dsra": dsra, "withdrawal": withdrawal, "release": release, "dscr_12m": dscr_12m, "lockup": lockup, "default": default, "distributions": distributions, "equity_cf": equity_cf, "equity_irr": equity_irr }

