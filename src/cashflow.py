import pandas as pd
import numpy as np

def read_row(path, sheet, label):

    # Return the 70 per-period values of the row whose label (column A) matches

    df = pd.read_excel(path, sheet_name=sheet, header=None)
    labels = df[0].astype(str).str.strip()
    row = df[labels == label]
    return row.iloc[0, 3:].to_numpy(dtype=float)

def load_constants(path):
    constants = {
        "debt_service": read_row(path, "Debt", "Debt service P90 (pasted values)"),
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
        "equity_cashflow": read_row(path, "Returns", "Equity cash flow"),
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

    
    return {"net_mwh": net_mwh, "revenue": revenue, "ebitda": ebitda,"used":used, "expired":expired, "tax": tax, "cfads":cfads}