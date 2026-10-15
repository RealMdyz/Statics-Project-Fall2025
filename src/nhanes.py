"""
Reusable functions for loading and preparing the NHANES 2021-2023 data.

Used by the notebooks in notebooks/. Keeping this logic in one place means
every notebook builds the analytic sample in exactly the same way.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

# Columns kept from each raw file
COLUMNS = {
    "DEMO_L": ["SEQN", "RIAGENDR", "RIDAGEYR", "WTINT2YR", "SDMVPSU", "SDMVSTRA"],
    "SLQ_L": ["SEQN", "SLD012", "SLD013"],
    "SMQ_L": ["SEQN", "SMQ020", "SMQ040", "SMD650"],
}

MIN_AGE = 18
SHORT_SLEEP_HOURS = 7


def load_raw(name: str) -> pd.DataFrame:
    """Read one NHANES .xpt file and keep only the columns we need."""
    df = pd.read_sas(RAW_DIR / f"{name}.xpt", format="xport")
    df = df[COLUMNS[name]].copy()
    df["SEQN"] = df["SEQN"].astype(int)
    return df


def merge_files(demo: pd.DataFrame, slq: pd.DataFrame, smq: pd.DataFrame) -> pd.DataFrame:
    """
    Left-join sleep and smoking onto demographics using SEQN.

    DEMO_L is the base because it contains every participant and the weights.
    validate="one_to_one" stops with an error if any SEQN is duplicated.
    """
    merged = demo.merge(slq, on="SEQN", how="left", validate="one_to_one")
    merged = merged.merge(smq, on="SEQN", how="left", validate="one_to_one")
    return merged


def smoking_status(smq020: float, smq040: float) -> str | float:
    """
    Never   : SMQ020 = 2 (has not smoked 100 cigarettes in life)
    Former  : SMQ020 = 1 and SMQ040 = 3 (not at all now)
    Current : SMQ020 = 1 and SMQ040 = 1 or 2 (every day / some days)
    Anything else (refused 7, don't know 9, missing) -> NaN
    """
    if smq020 == 2:
        return "never"
    if smq020 == 1 and smq040 == 3:
        return "former"
    if smq020 == 1 and smq040 in (1, 2):
        return "current"
    return np.nan


def add_derived_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Create the variables used in the analysis."""
    df = df.copy()
    df["sex"] = df["RIAGENDR"].map({1: "male", 2: "female"})
    df["smoking_status"] = [smoking_status(a, b) for a, b in zip(df["SMQ020"], df["SMQ040"])]
    df["smoking_status"] = pd.Categorical(
        df["smoking_status"], categories=["never", "former", "current"], ordered=False
    )
    # Weekly average: 5 workdays + 2 non-workdays
    df["sleep_weekly"] = (5 * df["SLD012"] + 2 * df["SLD013"]) / 7
    df["short_sleep"] = np.where(
        df["sleep_weekly"].notna(), (df["sleep_weekly"] < SHORT_SLEEP_HOURS).astype(float), np.nan
    )
    # Cigarettes per day: 777 = refused, 999 = don't know -> missing
    df["cigs_per_day"] = df["SMD650"].where(~df["SMD650"].isin([777, 999]))
    # Flag NHANES bottom/top codes: 2 = less than 3 h, 14 = 14 h or more
    df["sleep_coded_extreme"] = df["SLD012"].isin([2, 14]) | df["SLD013"].isin([2, 14])
    return df


def build_analytic_sample(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Apply the inclusion criteria step by step and record how many people
    remain after each step (the 'flow table' required in Phase 1, task A.4).
    """
    steps = []
    current = df
    steps.append(("All NHANES 2021-2023 participants", len(current)))

    current = current[current["RIDAGEYR"] >= MIN_AGE]
    steps.append((f"Aged {MIN_AGE} or older", len(current)))

    current = current[current["smoking_status"].notna()]
    steps.append(("Valid smoking status (excludes refused / don't know / missing)", len(current)))

    current = current[current["sleep_weekly"].notna()]
    steps.append(("Both weekday and weekend sleep hours available", len(current)))

    flow = pd.DataFrame(steps, columns=["step", "n_remaining"])
    flow["n_excluded"] = (-flow["n_remaining"].diff()).fillna(0).astype(int)
    return current.reset_index(drop=True), flow


# ---------------------------------------------------------------------------
# Weighted descriptive statistics (NHANES sampling weights)
# ---------------------------------------------------------------------------
def weighted_mean(x: pd.Series, w: pd.Series) -> float:
    """Sum(w * x) / Sum(w), ignoring rows where x is missing."""
    mask = x.notna() & w.notna()
    return float(np.average(x[mask], weights=w[mask]))


def weighted_quantile(x: pd.Series, w: pd.Series, q: float) -> float:
    """
    Weighted quantile: the value below which a share q of the total weight lies.
    Each person counts as many times as the number of people they represent.
    """
    mask = x.notna() & w.notna()
    xs, ws = x[mask].to_numpy(), w[mask].to_numpy()
    order = np.argsort(xs)
    xs, ws = xs[order], ws[order]
    cum = np.cumsum(ws) / ws.sum()
    return float(xs[np.searchsorted(cum, q)])


def weighted_share(condition: pd.Series, w: pd.Series) -> float:
    """Weighted proportion of rows where condition is True."""
    return float(w[condition].sum() / w.sum())
