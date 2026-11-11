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
        "dsra_depleted": bool(np.any((shortfall - r["withdrawal"])[repay] > 1)), # DSRA paid less than the shortfall (1 USD tolerance)
        "sponsor_support": -1 * np.sum(r["distributions"][repay][r["distributions"][repay] < 0]), # Equity injected by the sponsors during the loan
        "equity_irr": r["equity_irr"], # Equity IRR
       }


def simulate(table, c, n_sims, L, rng, n_years=30):
    """Run n_sims block-bootstrap trajectories and return one row of results per trajectory."""
    rows = []
    for i in range(n_sims):
        positions = block_bootstrap(len(table), n_years, L, rng)
        r = run_trajectory(table[positions].ravel(), c)
        row = summarize_trajectory(r, c)
        n_loan_years = int(c["repayment_flag"].sum() // 2)                 # 24 semesters -> 12 years
        annual = table[positions].sum(axis=1)[:n_loan_years]                 # energy of each loan year (GWh)
        dry = annual < np.median(table.sum(axis=1))                          # D5: dry = below the record median
        row["longest_dry_run"] = longest_run(dry)
        row["min_annual_energy"] = annual.min()
        rows.append(row)
    return pd.DataFrame(rows)

def longest_run(flags):
    """Length of the longest sequence of consecutive True values (e.g. consecutive dry years)."""
    longest = 0
    current = 0
    for f in flags:
        if f:
            current = current + 1      # one more dry year in the current run
        else:
            current = 0      # the run is broken
        longest = max(longest, current)          # keep the biggest run seen so far
    return longest