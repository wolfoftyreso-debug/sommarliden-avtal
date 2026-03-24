#!/usr/bin/env python3
"""Generera kvittosammanställning PDF för TryggBil Stockholm AB"""

from pathlib import Path
from weasyprint import HTML, CSS

BASE = Path(__file__).parent
OUT = BASE / "pdf"
OUT.mkdir(exist_ok=True)

TRANSACTIONS = [
    {"datum": "2026-02-24", "leverantör": "Uber",              "belopp": 99.00,     "valuta": "SEK", "kategori": "Transport"},
    {"datum": "2026-02-23", "leverantör": "Lovable",           "belopp": 4692.19,   "valuta": "SEK", "kategori": "Mjukvarutjänst"},
    {"datum": "2026-02-18", "leverantör": "One.com",           "belopp": 298.75,    "valuta": "SEK", "kategori": "Hosting/Domän"},
    {"datum": "2026-02-18", "leverantör": "Bandicam Company",  "belopp": 305.83,    "valuta": "SEK", "kategori": "Mjukvarutjänst"},
    {"datum": "2026-02-15", "leverantör": "Uber",              "belopp": 351.00,    "valuta": "SEK", "kategori": "Transport"},
    {"datum": "2026-02-15", "leverantör": "Uber",              "belopp": 276.00,    "valuta": "SEK", "kategori": "Transport"},
    {"datum": "2026-02-??", "leverantör": "Shotstack PTY",     "belopp": 1382.44,   "valuta": "SEK", "kategori": "Mjukvarutjänst"},
    {"datum": "2026-02-08", "leverantör": "Suno Inc.",         "belopp": 1125.00,   "valuta": "SEK", "kategori": "Mjukvarutjänst"},
    {"datum": "2026-02-07", "leverantör": "Refurbed",          "belopp": 8341.00,   "valuta": "SEK", "kategori": "Hårdvara"},
    {"datum": "2026-02-??", "leverantör": "Resend",            "belopp": 184.96,    "valuta": "SEK", "kategori": "Mjukvarutjänst", "not": "20 USD"},
    {"datum": "2026-02-04", "leverantör": "One.com",           "belopp": 2748.75,   "valuta": "SEK", "kategori": "Hosting/Domän"},
    {"datum": "2026-02-02", "leverantör": "Adobe",             "belopp": 372.93,    "valuta": "SEK", "kategori": "Mjukvarutjänst"},
    {"datum": "2026-02-02", "leverantör": "Adobe",             "belopp": 210.00,    "valuta": "SEK", "kategori": "Mjukvarutjänst"},
    {"datum": "2026-01-28", "leverantör": "Synthesia Limited", "belopp": 5449.17,   "valuta": "SEK", "kategori": "Mjukvarutjänst", "not": "597,38 USD"},
    {"datum": "2025-12-22", "leverantör": "One.com",           "belopp": 8293.75,   "valuta": "SEK", "kategori": "Hosting/Domän"},
    {"datum": "2025-12-19", "leverantör": "Ionos Cloud",       "belopp": 492.14,    "valuta": "SEK", "kategori": "Hosting/Domän", "not": "38,89 GBP"},
]

total = sum(t["belopp"] for t in TRANSACTIONS)

rows = ""
for i, t in enumerate(TRANSACTIONS):
    bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
    not_text = t.get("not", "")
    not_cell = f'<span style="font-size:10px;color:#888;margin-left:6px;">({not_text})</span>' if not_text else ""
    rows += f"""
    <tr style="background:{bg};">
      <td style="padding:10px 14px;font-size:13px;color:#64748b;white-space:nowrap;">{t['datum']}</td>
      <td style="padding:10px 14px;font-size:13px;font-weight:500;color:#1a1a2e;">{t['leverantör']}{not_cell}</td>
      <td style="padding:10px 14px;font-size:12px;color:#64748b;">{t['kategori']}</td>
      <td style="padding:10px 14px;font-size:13px;font-weight:600;color:#1a1a2e;text-align:right;">{t['belopp']:,.2f} kr</td>
    </tr>"""

html_content = f"""<!DOCTYPE html>
<html lang="sv">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;font-family:Arial,sans-serif;background:#fff;color:#1a1a2e;">

  <!-- Header -->
  <div style="background:#0A1628;padding:36px 48px;color:white;">
    <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#7090b0;margin-bottom:8px;">
      Trygg Bil Stockholm AB — Kortutlägg
    </div>
    <div style="font-size:24px;font-weight:700;margin-bottom:4px;">Kvittosammanställning</div>
    <div style="font-size:13px;color:#8aa0b8;">December 2025 – Februari 2026</div>
    <div style="margin-top:16px;font-size:12px;color:#8aa0b8;">
      Redovisad av: Erik Svensson &nbsp;·&nbsp; erik@hypbit.com<br>
      Datum: 2026-03-24 &nbsp;·&nbsp; Org.nr 559141-7042
    </div>
  </div>

  <!-- Info-box -->
  <div style="background:#eff6ff;border-left:4px solid #1D6FEB;margin:32px 48px 0;padding:14px 20px;border-radius:0 6px 6px 0;font-size:13px;color:#1e40af;">
    Dessa transaktioner är genomförda med Trygg Bil Stockholm ABs företagskort inom ramen för konsultuppdraget. 
    Samtliga poster avser verksamhetsrelaterade kostnader.
  </div>

  <!-- Tabell -->
  <div style="margin:24px 48px;">
    <table style="width:100%;border-collapse:collapse;border-radius:8px;overflow:hidden;border:1px solid #e2e8f0;">
      <thead>
        <tr style="background:#1D6FEB;">
          <th style="padding:12px 14px;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:white;text-align:left;font-weight:600;">Datum</th>
          <th style="padding:12px 14px;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:white;text-align:left;font-weight:600;">Leverantör</th>
          <th style="padding:12px 14px;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:white;text-align:left;font-weight:600;">Kategori</th>
          <th style="padding:12px 14px;font-size:11px;letter-spacing:1px;text-transform:uppercase;color:white;text-align:right;font-weight:600;">Belopp (SEK)</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
      <tfoot>
        <tr style="background:#0A1628;">
          <td colspan="3" style="padding:14px;font-size:13px;font-weight:700;color:white;">TOTALT</td>
          <td style="padding:14px;font-size:15px;font-weight:700;color:white;text-align:right;">{total:,.2f} kr</td>
        </tr>
      </tfoot>
    </table>
  </div>

  <!-- Footer -->
  <div style="margin:32px 48px;padding-top:16px;border-top:1px solid #e2e8f0;font-size:11px;color:#94a3b8;text-align:center;">
    Sommarliden Holding AB · Org.nr 559141-7042 · Åvägen 9, 135 48 Tyresö · erik@hypbit.com<br>
    Konfidentiellt — Trygg Bil Stockholm AB
  </div>

</body>
</html>"""

CSS_STYLE = CSS(string="""
@page {
    size: A4;
    margin: 15mm 0 15mm 0;
}
""")

output_path = OUT / "Kvittosammanstallning_TryggBil_Dec2025-Feb2026.pdf"
HTML(string=html_content).write_pdf(str(output_path), stylesheets=[CSS_STYLE])
print(f"✓ {output_path.name}")
print(f"  Totalt: {total:,.2f} kr ({len(TRANSACTIONS)} poster)")
