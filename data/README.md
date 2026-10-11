# Data

**Source:** CDC / NCHS — National Health and Nutrition Examination Survey (NHANES), cycle August 2021 – August 2023
**Official page:** https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023
**Analytic guidance:** https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/overviewbrief.aspx?Cycle=2021-2023

Raw files are NOT stored in this repository. Download them (SAS transport `.xpt`) into `data/raw/`.

| File | Component | Used for | Download date |
|---|---|---|---|
| `DEMO_L` | Demographics | age, sex, weights, design vars | _fill_ |
| _fill_ | | | |

**Merge key:** `SEQN` (respondent sequence number, one row per person)

## Rebuilding the analytic dataset
_Steps will be added once loading code exists (see `src/`)._
