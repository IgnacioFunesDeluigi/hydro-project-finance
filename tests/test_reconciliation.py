import numpy as np
import pandas as pd
import pytest

from src.cashflow import load_constants, read_row, run_trajectory

FIXTURES = [
    "model/hydro_pf_model_v1.xlsx",
    "tests/fixtures/p50_p90debt.xlsx",
    "tests/fixtures/eco20_p90debt.xlsx",
    "tests/fixtures/tariff100_p90.xlsx",
    "tests/fixtures/eco20_sized.xlsx",
    "tests/fixtures/p50_sized.xlsx",
]


def read_value(path, sheet, label):
    """Return the single value in column C of the row whose label matches."""
    df = pd.read_excel(path, sheet_name=sheet, header=None)
    labels = df[0].astype(str).str.strip()
    return df[labels == label].iloc[0, 2]


def case_energy(path):
    """60 semiannual energies (S1, S2, ...) of the case selected in the file."""
    s1 = read_value(path, "Operations", "Case energy Oct–Mar")
    s2 = read_value(path, "Operations", "Case energy Apr–Sep")
    return np.tile([s1, s2], 30)


@pytest.mark.parametrize("path", FIXTURES)
def test_reconciliation(path):
    c = load_constants(path)
    r = run_trajectory(case_energy(path), c)
    np.testing.assert_allclose(r["cfads"], read_row(path, "Tax", "CFADS"), rtol=1e-3, atol=1)
    np.testing.assert_allclose(r["dscr_12m"], read_row(path, "Cashflow", "12-month DSCR"), rtol=1e-3, atol=1e-6)
    np.testing.assert_allclose(r["equity_irr"], read_value(path, "Returns", "Equity IRR (annual)"), rtol=1e-3)
    np.testing.assert_allclose(r["lockup"], read_row(path, "Cashflow", "Lock-up flag"), rtol=1e-3)
    np.testing.assert_allclose(r["default"], read_row(path, "Cashflow", "Default flag (info)"), rtol=1e-3)
    np.testing.assert_allclose(r["distributions"], read_row(path, "Cashflow", "− Distributions (negative = equity injection)"), rtol=1e-3, atol=1)
    np.testing.assert_allclose(r["withdrawal"], read_row(path, "Cashflow", "− Withdrawal"), rtol=1e-3, atol=1)



