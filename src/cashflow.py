import pandas as pd


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