# Statistics Course Project — Fall 1405 (2026)

**Title:** Cigarette smoking status and self-reported sleep duration among U.S. adults (NHANES 2021–2023)
**Track:** A — NHANES August 2021 – August 2023
**Author:** Mohammad Yasin Zare

## Research question
Among U.S. adults aged 18+, do weekly average sleep duration and the share of short sleep (< 7 h/night)
differ between never, former and current cigarette smokers? Does the difference remain after accounting
for age and sex? Among current smokers, is the number of cigarettes per day related to sleep duration?

Full statistical framing: [`PROJECT_CARD.md`](PROJECT_CARD.md) (Persian).

## Key Phase 1 result (descriptive only)
| Smoking status | n | Mean weekly sleep (h) | Short sleep, weighted |
|---|---|---|---|
| Never | 4,823 | 7.95 | 16.8% |
| Former | 2,020 | 7.88 | 20.3% |
| Current | 1,153 | 7.72 | 27.7% |

Differences are unadjusted and no inferential test has been applied yet (Phase 3).

## How to reproduce
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
python src/download_data.py     # downloads DEMO_L, SLQ_L, SMQ_L from CDC into data/raw/
```
Then run the notebooks **in order**:

| Notebook | What it does | Phase 1 tasks |
|---|---|---|
| `notebooks/01_load_and_merge.ipynb` | Load, merge on `SEQN`, derive variables, build analytic sample + flow table | 2, A.1, A.4 |
| `notebooks/02_data_quality.ipynb` | Missing data, special codes, ranges, logical consistency, quality table | 5 |
| `notebooks/03_descriptive_stats.ipynb` | Frequency tables, center/spread, 6 figures, group comparison, weighted vs unweighted | 6, 7, 8, 9, A.3 |

Optional: `python src/build_report.py` re-renders the report PDF (needs `playwright`).

## Repository layout
| Path | Content |
|---|---|
| `PROJECT_CARD.md` | Statistical framing of the project (Persian) |
| `data/README.md` | Data source, files, download date, rebuild steps |
| `src/download_data.py` | Reproducible download of raw NHANES files |
| `src/nhanes.py` | Shared loading, merging, variable derivation, analytic sample, weighted statistics |
| `src/build_report.py` | Renders the report HTML to PDF |
| `notebooks/` | Analysis notebooks, run in numeric order |
| `figures/` | Final figures used in the reports |
| `reports/phase1.pdf` | **Phase 1 report (Persian)** |
| `reports/phase1/` | Phase 1 tables (CSV) and report source |

Raw and processed data are **not** stored in this repository (see `.gitignore`).

## Phase status
| Phase | Deadline | Tag | Status |
|---|---|---|---|
| 1 — Data & descriptive statistics | 12 Aban 1405 | `phase-1` | ✅ done |
| 2 — Probability | 27 Aban 1405 | `phase-2` | — |
| 3 — Inference | 27 Azar 1405 | `phase-3` | — |
| 4 — Regression | 15 Dey 1405 | `phase-4` | — |
| 5 — Robustness & final | 5 Bahman 1405 | `phase-5-final` | — |
