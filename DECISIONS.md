# Decisions

## D1 · 2026-10-15 · Research question
Decision: size debt at P90 energy from daily streamflow; thesis storm methods move to a v2 flood module.
Why: design storms drive flood peaks, not annual energy yield.
Source: project roadmap, section 1.

## D2 · 2026-10-15 · Python version
Decision: dedicated conda environment "hydro" from conda-forge, Python pinned to 3.13.
why: pandas supports Python 3.14 only since 2.3.3; 3.13 has a longer track record and lowers the risk that later libraries (e.g. PyTorch in phase 6) lack 3.14 builds.
Source: https://pandas.pydata.org/pandas-docs/version/2.3/whatsnew/v2.3.3.html (EST; PyTorch 3.14 support: VERIFICAR)
