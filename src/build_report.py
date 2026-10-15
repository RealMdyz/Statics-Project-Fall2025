"""
Render reports/phase1/phase1_report.html to reports/phase1.pdf.

Optional tool (not needed to reproduce the analysis):
    pip install playwright && playwright install chromium
    python src/build_report.py
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "reports" / "phase1" / "phase1_report.html"
OUT = ROOT / "reports" / "phase1.pdf"


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(SRC.as_uri())
        await page.wait_for_timeout(800)
        await page.pdf(
            path=str(OUT), format="A4", print_background=True,
            display_header_footer=True, header_template="<span></span>",
            footer_template='<div style="width:100%;text-align:center;font-size:8pt;color:#888;">'
                            '<span class="pageNumber"></span> / <span class="totalPages"></span></div>',
            margin={"top": "20mm", "bottom": "18mm", "left": "18mm", "right": "18mm"},
        )
        await browser.close()
    print(f"Saved {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
