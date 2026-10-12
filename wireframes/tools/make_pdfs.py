"""Generates the three placeholder supporting documents in wireframes/docs/.
Run from the wireframes folder:  python3 tools/make_pdfs.py
Figures are derived from the line items so they cannot drift from each other.
"""
import os

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")


def make_pdf(path, lines):
    def esc(t):
        return t.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    y, ops = 790, []
    for text, size, font in lines:
        if text is None:
            y -= size
            continue
        ops.append(f"BT /{font} {size} Tf 56 {y} Td ({esc(text)}) Tj ET")
        y -= size * 1.5
    content = "\n".join(ops).encode("latin-1")
    fonts = {"F1": "Helvetica", "F2": "Helvetica-Bold", "F3": "Courier", "F4": "Courier-Bold"}
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R /F4 7 0 R >> >> /Contents 8 0 R >>"]
    for k in ["F1", "F2", "F3", "F4"]:
        objs.append(f"<< /Type /Font /Subtype /Type1 /BaseFont /{fonts[k]} /Encoding /WinAnsiEncoding >>".encode())
    objs.append(b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream")
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for o in offs:
        out += b"%010d 00000 n \n" % o
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
    with open(os.path.join(DOCS, path), "wb") as fh:
        fh.write(out)


H = lambda t: (t, 16, "F2"); S = lambda t: (t, 11, "F2"); L = lambda t: (t, 10, "F1")
M = lambda t: (t, 9, "F3"); MB = lambda t: (t, 9, "F4"); B = (None, 8, "F1")
f = lambda v: f"{v:,.2f}"

# ---- Figures ------------------------------------------------------------
ITEMS = [("RMS Version 5 application licence (named user)", 450, 1200.00),
         ("Rack server, 2-node application cluster", 2, 48500.00),
         ("Storage array, 120 TB usable", 1, 185000.00),
         ("Implementation and data migration services", 1, 312500.00),
         ("User training, 30 pax per session", 15, 3000.00),
         ("Annual maintenance and support, Year 1", 1, 105000.00)]
SUBS = [q * u for _, q, u in ITEMS]
TOTAL = sum(SUBS)
BUDGET_AVAILABLE = 2450000.00

# Cashflow as entered on the form (Charging page). Must match the HTML pages.
FORM_CASHFLOW = {"Q3 FY2026": SUBS[0] + SUBS[1],          # 637,000.00
                 "Q4 FY2026": SUBS[2] + SUBS[3],          # 497,500.00
                 "Q1 FY2027": SUBS[4] + SUBS[5]}          # 150,000.00

# Payment milestones in the vendor quotation. Deliberately differs from the
# form's cashflow in Q4 FY2026 and Q1 FY2027: this is the discrepancy the
# approver flags on the Charging page.
QUOTE_MILESTONES = {"Q3 FY2026": SUBS[0] + SUBS[1],                      # 637,000.00
                    "Q4 FY2026": SUBS[2],                                # 185,000.00
                    "Q1 FY2027": SUBS[3] + SUBS[4] + SUBS[5]}            # 462,500.00

# ---- Checks -------------------------------------------------------------
assert TOTAL == 1284500.00, TOTAL
assert sum(FORM_CASHFLOW.values()) == TOTAL, FORM_CASHFLOW
assert sum(QUOTE_MILESTONES.values()) == TOTAL, QUOTE_MILESTONES
assert FORM_CASHFLOW["Q4 FY2026"] != QUOTE_MILESTONES["Q4 FY2026"], "flag on Charging page would no longer be valid"
assert BUDGET_AVAILABLE - TOTAL == 1165500.00

# ---- 1. Vendor quotation ------------------------------------------------
make_pdf("RMS_v5_Vendor_Quotation_Q-26-0418.pdf", [
    H("Meridian Systems Pte Ltd"),
    L("12 Tampines Industrial Crescent, #05-01, Singapore 528606   GST Reg. No. M2-0417892-3"), B,
    S("QUOTATION  Q-26-0418"),
    L("Date: 30 Sep 2026        Valid until: 30 Nov 2026"),
    L("To: Tan Wei Ling, Senior Executive (Information Systems), National Records Agency"),
    L("Subject: Upgrade of Records Management System (RMS) to Version 5"), B,
    MB("S/N  Item                                              Qty    Unit (S$)    Amount (S$)")]
    + [M(f"{i}    {n:<48}{q:>5}  {f(u):>11}  {f(s):>13}") for i, ((n, q, u), s) in enumerate(zip(ITEMS, SUBS), 1)]
    + [MB(f"     Total, inclusive of 9% GST{'':<42}{f(TOTAL):>13}"), B,
    S("Payment milestones"),
    M(f"On delivery of licences and servers (items 1, 2)          Oct-Dec 2026   {f(QUOTE_MILESTONES['Q3 FY2026']):>13}"),
    M(f"On delivery of storage array (item 3)                     Jan-Mar 2027   {f(QUOTE_MILESTONES['Q4 FY2026']):>13}"),
    M(f"On go-live: migration, training, maintenance (items 4-6)  Apr-Jun 2027   {f(QUOTE_MILESTONES['Q1 FY2027']):>13}"),
    MB(f"     Total{'':<62}{f(TOTAL):>13}"), B,
    S("Terms"),
    L("1. Delivery: hardware within 8 weeks of purchase order. Migration completed within 20 weeks."),
    L("2. Prices are firm for the validity period and subject to the Government Supplier Terms."), B,
    L("Prepared by: Daniel Koh, Account Manager, Meridian Systems Pte Ltd"),
    L("This is a placeholder document generated for a wireframe case study."),
])

# ---- 2. Internal audit extract -----------------------------------------
make_pdf("Internal_Audit_Report_Extract.pdf", [
    H("National Records Agency - Internal Audit"),
    L("Annual Internal Audit Report, FY2025: Review of IT Systems and Information Security"),
    L("Issued 18 Mar 2026. Extract: Finding 3 only. Classification: Restricted"), B,
    S("Finding 3 - Records Management System (RMS) is unsupported and not secure"),
    L("Rating: High"), B,
    S("Observation"),
    L("The RMS is running Version 3.2, for which vendor support ended on 30 Jun 2026. Unsupported"),
    L("software no longer receives security patches and does not meet the Government's current"),
    L("security requirements for supported software and vulnerability management."),
    L("The RMS storage array was at 91% of capacity at the time of audit. The FY2026 digitisation"),
    L("intake of approximately 18 TB cannot be accommodated without expansion."), B,
    S("Risk"),
    L("Loss or compromise of agency records; inability to ingest new digitised records; adverse"),
    L("findings in the next Government security compliance review."), B,
    S("Recommendation"),
    L("Management should upgrade the RMS to a vendor-supported version and replace the storage"),
    L("array before the FY2026 digitisation programme commences. Interim support should be"),
    L("arranged if the upgrade cannot be completed within FY2026."), B,
    S("Management response"),
    L("Agreed. Information Systems Department will submit a budget request for the RMS Version 5"),
    L("upgrade in FY2026. Target completion: Q1 FY2027. Owner: Deputy Director (Information Systems)."), B,
    L("This is a placeholder document generated for a wireframe case study."),
])

# ---- 3. Cost breakdown (matches the form) -------------------------------
make_pdf("RMS_Upgrade_Cost_Breakdown_FY2026.pdf", [
    H("RMS Upgrade - Cost Breakdown and Cashflow, FY2026"),
    L("Submission ES-2026-000347   Prepared by Tan Wei Ling, Information Systems Department   06 Oct 2026"), B,
    S("A. Cost components (SGD, inclusive of GST)"),
    M(f"1  RMS Version 5 application licence, 450 named users x 1,200.00    {f(SUBS[0]):>15}"),
    M(f"2  Rack server, 2-node application cluster, 2 x 48,500.00            {f(SUBS[1]):>15}"),
    M(f"3  Storage array, 120 TB usable, 1 x 185,000.00                     {f(SUBS[2]):>15}"),
    M(f"4  Implementation and data migration services                       {f(SUBS[3]):>15}"),
    M(f"5  User training, 15 sessions x 3,000.00                            {f(SUBS[4]):>15}"),
    M(f"6  Annual maintenance and support, Year 1                           {f(SUBS[5]):>15}"),
    MB(f"   Total amount requested                                          {f(TOTAL):>15}"), B,
    S("B. Cashflow by quarter"),
    M(f"FY2026 Q3 (Oct-Dec 2026)  Licences and servers (items 1, 2)           {f(FORM_CASHFLOW['Q3 FY2026']):>15}"),
    M(f"FY2026 Q4 (Jan-Mar 2027)  Storage and implementation (items 3, 4)     {f(FORM_CASHFLOW['Q4 FY2026']):>15}"),
    M(f"FY2027 Q1 (Apr-Jun 2027)  Training and Year 1 maintenance (items 5, 6){f(FORM_CASHFLOW['Q1 FY2027']):>15}"),
    MB(f"   Total                                                          {f(TOTAL):>15}"), B,
    S("C. Charging"),
    L("Cost centre: Information Systems Department"),
    L("Fund: IT Systems Fund, FY2026        Expense category: IT equipment and software"),
    L(f"Budget available: S${f(BUDGET_AVAILABLE)}     Remaining after approval: S${f(BUDGET_AVAILABLE - TOTAL)}"), B,
    S("D. Basis"),
    L("Figures taken from Meridian Systems quotation Q-26-0418 dated 30 Sep 2026, valid until 30 Nov 2026."),
    L("No payments fall in Q1 or Q2 FY2026 as the request was raised on 02 Oct 2026."), B,
    L("This is a placeholder document generated for a wireframe case study."),
])

print("Total", f(TOTAL))
print("Form cashflow     ", {k: f(v) for k, v in FORM_CASHFLOW.items()})
print("Quote milestones  ", {k: f(v) for k, v in QUOTE_MILESTONES.items()})
