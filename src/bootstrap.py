import numpy as np
import pandas as pd

from src.cashflow import run_trajectory


def block_bootstrap(n_records, n_years, L, rng):
    """Return the positions (0 to n_records - 1) of n_years years drawn in circular blocks of length L."""
    n_blocks = int(np.ceil(n_years / L))                     # how many blocks you need to reach n_years
    starts = rng.integers(0, n_records, size=n_blocks)       # random start position of each block
    positions = []
    for start in starts:
        for j in range(L):
            positions.append((start + j)% n_records)        # the year j places after start, wrapping around
    return np.array(positions[:n_years])                    # cut the extra years of the last block


def summarize_trajectory(r, c):
    """Results of one simulated trajectory (one row of the results table)."""
    repay = c["repayment_flag"] == 1
    shortfall = np.maximum(0, c["debt_service"] - r["cfads"])   # cash missing to pay debt service
    return {
        "min_dscr_12m": float(np.min(r["dscr_12m"][repay])), # Minimum DSCR in repay period
        "any_lockup": bool(r["lockup"].sum() > 0),  # If there was any lockup event
        "lockup_semesters": int(np.sum(r["lockup"] == 1 )) ,  # How many semesters in total, were lockups
        "any_default": bool(r["default"].sum() > 0),  # If there was any default event
        "dsra_depleted": bool(np.any(shortfall - r["withdrawal"] > 1)),   # DSRA paid less than the shortfall (1 USD tolerance)
        "sponsor_support": -1 * np.sum(r["distributions"][r["distributions"] < 0]),
        "equity_irr": r["equity_irr"],
    }


def simulate(table, c, n_sims, L, rng, n_years=30):
    """Run n_sims block-bootstrap trajectories and return one row of results per trajectory."""
    rows = []
    for i in range(n_sims):
        positions = block_bootstrap(len(table), n_years, L, rng)
        r = run_trajectory(table[positions].ravel(), c)
        rows.append(summarize_trajectory(r, c))
    return pd.DataFrame(rows)