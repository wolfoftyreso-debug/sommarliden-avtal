#!/usr/bin/env python3
"""Generera enterprise-grade PDF:er från Markdown-avtal och fakturor."""

import os
import re
from pathlib import Path
from weasyprint import HTML, CSS

BASE = Path(__file__).parent
OUT = BASE / "pdf"
OUT.mkdir(exist_ok=True)

CSS_STYLE = CSS(string="""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

@page {
    size: A4;
    margin: 30mm 25mm 35mm 25mm;
    @top-left {
        content: "Sommarliden Holding AB  ·  Org.nr 559141-7042";
        font-family: Arial, sans-serif;
        font-size: 8pt;
        color: #888;
        padding-top: 10mm;
    }
    @top-right {
        content: string(doc-ref);
        font-family: Arial, sans-serif;
        font-size: 8pt;
        color: #888;
        padding-top: 10mm;
    }
    @bottom-left {
        content: "Konfidentiellt — Sommarliden Holding AB";
        font-family: Arial, sans-serif;
        font-size: 7.5pt;
        color: #aaa;
    }
    @bottom-right {
        content: "Sida " counter(page) " av " counter(pages);
        font-family: Arial, sans-serif;
        font-size: 8pt;
        color: #888;
    }
    @bottom-center {
        content: "";
        border-top: 0.5pt solid #ccc;
        width: 100%;
    }
}

@page :first {
    @top-left { content: ""; }
    @top-right { content: ""; }
}

* { box-sizing: border-box; }

body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10.5pt;
    line-height: 1.7;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}

/* ====== HEADER BLOCK (första sidan) ====== */
.doc-header {
    border-bottom: 3px solid #0d2240;
    padding-bottom: 16px;
    margin-bottom: 28px;
    page-break-after: avoid;
}

.doc-header .company-name {
    font-size: 15pt;
    font-weight: 700;
    color: #0d2240;
    letter-spacing: 0.3px;
}

.doc-header .company-meta {
    font-size: 8.5pt;
    color: #666;
    margin-top: 2px;
}

.doc-header .doc-title {
    font-size: 20pt;
    font-weight: 700;
    color: #0d2240;
    margin-top: 18px;
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}

.doc-header .doc-subtitle {
    font-size: 9.5pt;
    color: #666;
    font-style: italic;
}

/* ====== RUBRIKER ====== */
h1 {
    font-size: 17pt;
    font-weight: 700;
    color: #0d2240;
    border-bottom: 2px solid #0d2240;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 24px;
    page-break-after: avoid;
    string-set: doc-ref content();
}

h2 {
    font-size: 11.5pt;
    font-weight: 700;
    color: #0d2240;
    margin-top: 32px;
    margin-bottom: 10px;
    padding-top: 16px;
    border-top: 1px solid #d0d8e4;
    page-break-after: avoid;
    page-break-inside: avoid;
}

h3 {
    font-size: 10.5pt;
    font-weight: 600;
    color: #333;
    margin-top: 16px;
    margin-bottom: 6px;
    page-break-after: avoid;
}

/* ====== TABELLER ====== */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 20px 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

thead th {
    background: #0d2240;
    color: #ffffff;
    padding: 9px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 9.5pt;
    letter-spacing: 0.2px;
}

tbody td {
    padding: 8px 12px;
    border-bottom: 1px solid #e0e6ef;
    vertical-align: top;
}

tbody tr:nth-child(even) td {
    background: #f4f7fb;
}

tbody tr:last-child td {
    border-bottom: 2px solid #0d2240;
}

tfoot td, .total-row td {
    background: #f0f4fa !important;
    font-weight: 700;
    border-top: 2px solid #0d2240;
    border-bottom: 2px solid #0d2240;
}

/* ====== INFO-BOXAR ====== */
.info-box {
    background: #f4f7fb;
    border-left: 4px solid #0d2240;
    padding: 14px 18px;
    margin: 18px 0;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
}

.warning-box {
    background: #fff8e6;
    border-left: 4px solid #e6a817;
    padding: 14px 18px;
    margin: 18px 0;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
}

/* ====== PARTER-SEKTION ====== */
.parties-grid {
    display: table;
    width: 100%;
    border: 1px solid #d0d8e4;
    border-radius: 4px;
    margin: 16px 0 24px 0;
    page-break-inside: avoid;
}

.party-col {
    display: table-cell;
    width: 50%;
    padding: 14px 18px;
    vertical-align: top;
}

.party-col:first-child {
    border-right: 1px solid #d0d8e4;
    background: #f8fafc;
}

.party-label {
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0d2240;
    margin-bottom: 6px;
}

/* ====== AVSNITT ====== */
.section {
    margin: 0 0 24px 0;
    page-break-inside: avoid;
}

/* ====== SIGNATURRUTA ====== */
.signature-block {
    margin-top: 40px;
    page-break-inside: avoid;
    border-top: 2px solid #0d2240;
    padding-top: 20px;
}

.sig-row {
    display: table;
    width: 100%;
    margin-top: 30px;
}

.sig-col {
    display: table-cell;
    width: 48%;
    padding-right: 4%;
    vertical-align: top;
}

.sig-line {
    border-bottom: 1px solid #333;
    margin-top: 40px;
    margin-bottom: 4px;
}

.sig-label {
    font-size: 9pt;
    color: #666;
}

/* ====== FAKTURA-SPECIFIKT ====== */
.invoice-meta {
    display: table;
    width: 100%;
    margin-bottom: 28px;
    page-break-inside: avoid;
}

.invoice-from {
    display: table-cell;
    width: 55%;
    vertical-align: top;
}

.invoice-to {
    display: table-cell;
    width: 45%;
    vertical-align: top;
    text-align: right;
}

.invoice-numbers {
    background: #0d2240;
    color: white;
    padding: 16px 20px;
    margin-bottom: 24px;
    display: table;
    width: 100%;
    page-break-inside: avoid;
}

.inv-num-cell {
    display: table-cell;
    width: 33%;
    text-align: center;
}

.inv-num-label {
    font-size: 8pt;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: block;
    margin-bottom: 3px;
}

.inv-num-value {
    font-size: 13pt;
    font-weight: 700;
    display: block;
}

.inv-total {
    font-size: 18pt;
    font-weight: 700;
    color: #0d2240;
    text-align: right;
    margin: 12px 0;
}

/* ====== PAYMENT BOX ====== */
.payment-box {
    background: #f0f4fa;
    border: 1px solid #c0cfe0;
    padding: 16px 20px;
    margin-top: 24px;
    page-break-inside: avoid;
}

.payment-box-title {
    font-size: 9pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #0d2240;
    margin-bottom: 10px;
}

/* ====== ÖVRIGT ====== */
hr {
    border: none;
    border-top: 1px solid #d0d8e4;
    margin: 20px 0;
}

strong { font-weight: 700; }
em { font-style: italic; }

p {
    margin: 6px 0 10px 0;
    orphans: 3;
    widows: 3;
}

ul, ol {
    margin: 8px 0 12px 0;
    padding-left: 22px;
}

li {
    margin-bottom: 4px;
    line-height: 1.6;
}

.page-break { page-break-before: always; }
.no-break { page-break-inside: avoid; }

.footer-note {
    font-size: 8.5pt;
    color: #888;
    font-style: italic;
    margin-top: 32px;
    padding-top: 12px;
    border-top: 1px solid #e0e6ef;
}
""")


def md_to_html(md_text, doc_type="generic", title="", ref=""):
    """Konvertera Markdown till enterprise-formaterad HTML."""

    html_body = md_text

    # --- Tabeller ---
    def convert_table(match):
        rows_raw = match.group(0).strip().split('\n')
        rows = [r for r in rows_raw if r.strip() and not re.match(r'^\|[-: |]+\|$', r.strip())]
        out = '<table><thead>'
        for i, row in enumerate(rows):
            cells = [c.strip() for c in row.strip('|').split('|')]
            if i == 0:
                out += '<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr></thead><tbody>'
            else:
                out += '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
        return out + '</tbody></table>'
    html_body = re.sub(r'(\|.+\|\n(\|[-: |]+\|\n)?)+(\|.+\|\n?)+', convert_table, html_body)

    # --- Rubriker ---
    html_body = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_body, flags=re.M)
    html_body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_body, flags=re.M)
    html_body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_body, flags=re.M)

    # --- Bold/italic ---
    html_body = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html_body)
    html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)
    html_body = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_body)

    # --- HR ---
    html_body = re.sub(r'^---$', '<hr>', html_body, flags=re.M)

    # --- Listor ---
    def convert_list(match):
        items = re.findall(r'^[-*] (.+)$', match.group(0), re.M)
        return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
    html_body = re.sub(r'(^[-*] .+\n?)+', convert_list, html_body, flags=re.M)

    # --- Paragrafer ---
    lines = html_body.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<') and not stripped.startswith('&'):
            result.append(f'<p>{stripped}</p>')
        else:
            result.append(line)
    html_body = '\n'.join(result)

    # --- Header block ---
    header_html = f"""
<div class="doc-header">
  <div class="company-name">Sommarliden Holding AB</div>
  <div class="company-meta">Org.nr 559141-7042 &nbsp;·&nbsp; Åvägen 9, 135 48 Tyresö &nbsp;·&nbsp; erik@hypbit.com</div>
  <div class="doc-title">{title}</div>
  {'<div class="doc-subtitle">Avtalsnr: ' + ref + '</div>' if ref else ''}
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
</head>
<body>
{header_html}
{html_body}
</body>
</html>"""


def get_title_and_ref(md_path):
    """Extrahera titel och referensnummer från filnamn."""
    name = md_path.stem
    if "Hyresavtal" in name:
        return "Hyresavtal — Lokal", "AVT-H-2026-001"
    elif "Konsultavtal" in name:
        return "Konsultavtal", "AVT-K-2026-001"
    elif "Faktura" in name:
        parts = name.split('_')
        num = parts[1] if len(parts) > 1 else ""
        period = ' '.join(parts[3:]).replace('2026', '2026').replace('2027', '2027') if len(parts) > 3 else ""
        kind = "Hyra" if "Hyra" in name else "Konsult"
        return f"Faktura {num} — {kind} {period}", f"REF-{num}"
    elif "Betalningsplan" in name:
        return "Betalningsplan 2026–2027", "BET-2026-001"
    elif "README" in name:
        return "Avtalspaket — Trygg Bil Stockholm AB", "PKT-2026-001"
    return name.replace('_', ' '), ""


def generate(md_path, out_path):
    text = md_path.read_text(encoding='utf-8')
    title, ref = get_title_and_ref(md_path)
    html = md_to_html(text, title=title, ref=ref)
    HTML(string=html, base_url=str(md_path.parent)).write_pdf(
        str(out_path),
        stylesheets=[CSS_STYLE],
        presentational_hints=True
    )
    print(f"  ✓ {out_path.name}")


print("Genererar enterprise PDF:er...")

# Avtal
for f in sorted((BASE / "avtal").glob("*.md")):
    generate(f, OUT / f"{f.stem}.pdf")

# Fakturor hyra
hyra_out = OUT / "fakturor" / "hyra"
hyra_out.mkdir(parents=True, exist_ok=True)
for f in sorted((BASE / "fakturor" / "hyra").glob("*.md")):
    generate(f, hyra_out / f"{f.stem}.pdf")

# Fakturor konsult
konsult_out = OUT / "fakturor" / "konsult"
konsult_out.mkdir(parents=True, exist_ok=True)
for f in sorted((BASE / "fakturor" / "konsult").glob("*.md")):
    generate(f, konsult_out / f"{f.stem}.pdf")

# Betalningsplan + README
generate(BASE / "Betalningsplan_TryggBil_2026-2027.md", OUT / "Betalningsplan_TryggBil_2026-2027.pdf")
generate(BASE / "README.md", OUT / "README.pdf")

print(f"\nKlart! PDF:er i: {OUT}")
