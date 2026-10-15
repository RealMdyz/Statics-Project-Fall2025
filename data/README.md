# Data

**Source:** CDC / NCHS — National Health and Nutrition Examination Survey (NHANES), cycle August 2021 – August 2023
**Official page:** https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023
**Analytic guidance:** https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/overviewbrief.aspx?Cycle=2021-2023
**Download date:** 2026-10-12 (20 Mehr 1405), recorded automatically in `data/raw/download_log.txt`

Raw files are **not** stored in this repository. Rebuild them with:

```bash
python src/download_data.py
```

| File | Component | Rows | Used for |
|---|---|---|---|
| `DEMO_L.xpt` | Demographics | 11,933 | age (`RIDAGEYR`), sex (`RIAGENDR`), interview weight (`WTINT2YR`), design variables (`SDMVPSU`, `SDMVSTRA`) |
| `SLQ_L.xpt` | Sleep Disorders questionnaire (16+) | 8,501 | weekday sleep (`SLD012`), weekend sleep (`SLD013`) |
| `SMQ_L.xpt` | Smoking – Cigarette Use questionnaire (12+) | 9,015 | ever 100 cigarettes (`SMQ020`), current smoking (`SMQ040`), cigarettes/day (`SMD650`) |

Direct URLs: `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/<FILE>.xpt`

**Merge key:** `SEQN` (one row per participant in every file).

## Rebuilding the analytic dataset
All steps are implemented in `src/nhanes.py` and run in `notebooks/01_load_and_merge.ipynb`:

1. Read the three `.xpt` files and keep the needed columns (`load_raw`).
2. Left-join sleep and smoking onto `DEMO_L` by `SEQN`, checking one-to-one (`merge_files`).
3. Derive variables (`add_derived_variables`):
   - `smoking_status`: never (`SMQ020`=2), former (`SMQ020`=1 & `SMQ040`=3), current (`SMQ020`=1 & `SMQ040`∈{1,2})
   - `sleep_weekly` = (5 × `SLD012` + 2 × `SLD013`) / 7
   - `short_sleep` = `sleep_weekly` < 7
   - `cigs_per_day` = `SMD650` with 777/999 set to missing
   - `sleep_coded_extreme` flags sleep codes 2 (< 3 h) and 14 (≥ 14 h)
4. Apply inclusion criteria in order (`build_analytic_sample`):

| Step | Remaining | Excluded |
|---|---|---|
| All participants | 11,933 | – |
| Age ≥ 18 | 8,153 | 3,780 |
| Valid smoking status | 8,121 | 32 |
| Weekday and weekend sleep available | **7,996** | 125 |

The analytic sample is written to `data/processed/analytic_sample.csv` (not committed).
