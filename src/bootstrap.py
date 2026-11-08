import numpy as np

def block_bootstrap(n_records, n_years, L, rng):
    """Return the positions (0 to n_records - 1) of n_years years drawn in circular blocks of length L."""
    n_blocks = int(np.ceil(n_years / L))                     # how many blocks you need to reach n_years
    starts = rng.integers(0, n_records, size=n_blocks)       # random start position of each block
    positions = []
    for start in starts:
        for j in range(L):
            positions.append((start + j)% n_records)        # the year j places after start, wrapping around
    return np.array(positions[:n_years])                    # cut the extra years of the last block
