"""
Download the raw NHANES 2021-2023 files used in this project into data/raw/.

Usage (from the repository root, with the virtual environment active):
    python src/download_data.py

Raw files are NOT committed to GitHub (see .gitignore). Anyone can rebuild
them by running this script. The download date is written to
data/raw/download_log.txt so it can be reported in data/README.md.
"""
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/"
FILES = {
    "DEMO_L": "Demographics: age, sex, sampling weights, design variables",
    "SLQ_L": "Sleep disorders questionnaire: usual sleep hours",
    "SMQ_L": "Smoking - cigarette use questionnaire",
}

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def download(name: str) -> int:
    url = f"{BASE_URL}{name}.xpt"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (student project)"})
    with urlopen(req, timeout=120) as resp:
        content = resp.read()
    (RAW_DIR / f"{name}.xpt").write_bytes(content)
    return len(content)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    log_lines = [f"Download date: {date.today().isoformat()}"]
    for name, description in FILES.items():
        size = download(name)
        line = f"{name}.xpt  {size / 1024:,.0f} KB  -  {description}"
        print(line)
        log_lines.append(line)
    (RAW_DIR / "download_log.txt").write_text("\n".join(log_lines) + "\n")
    print(f"\nSaved to: {RAW_DIR}")


if __name__ == "__main__":
    main()
