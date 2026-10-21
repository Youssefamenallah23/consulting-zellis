# -*- coding: utf-8 -*-
"""Evaluate the workbook with an independent engine and assert the numbers."""
import sys
from pathlib import Path

import formulas

sys.stdout.reconfigure(encoding="utf-8")

WB = Path(__file__).parent.parent / "model" / "ValueAtStake.xlsx"
book = formulas.ExcelModel().loads(str(WB)).finish()
sol = book.calculate()

P = "'[ValueAtStake.xlsx]"


def v(sheet_cell):
    sheet, cell = sheet_cell.split("!")
    key = P + sheet.upper() + "'!" + cell
    return sol[key].value[0, 0]


checks = {
    "Inputs rows": ("INPUTS!A5", None),
    "Target revenue": ("BENCHMARKS!D5", 261068),
    "Target FTE": ("BENCHMARKS!F5", 2655),
    "Target rev/FTE": ("BENCHMARKS!G5", 98.33),
    "Target staff %": ("BENCHMARKS!H5", 0.5228),
    "Peer median rev/FTE": ("BENCHMARKS!B12", 135.33),
    "Peer P25": ("BENCHMARKS!B13", 130.21),
    "Peer P75": ("BENCHMARKS!B14", 149.45),
    "Peer median staff %": ("BENCHMARKS!B15", 0.3995),
    "Gap %": ("BENCHMARKS!B21", -0.2733),
    "Method A": ("SIZING!B9", 32196),
    "Implied FTE": ("SIZING!B13", 1929.2),
    "Method B": ("SIZING!B16", 37310),
    "Reconciliation": ("SIZING!B20", 0.1588),
    "Verdict": ("SIZING!B21", "RECONCILED"),
    "Low": ("SIZING!B24", 32196),
    "High": ("SIZING!B25", 37310),
    "Mid": ("SIZING!B26", 34753),
    "Year-1 net": ("SIZING!B35", 12164),
    "Scenario cons": ("SCENARIOS!E5", 33425),
    "Scenario base": ("SCENARIOS!E6", 37310),
    "Scenario stretch": ("SCENARIOS!E7", 46684),
    "Sens top-left": ("SENSITIVITY!B5", 4343.68),
    "Sens bottom-right": ("SENSITIVITY!F8", 3475),
    "Checks overall": ("CHECKS!B17", "ALL CHECKS PASS"),
}

worst = 0.0
fails = []
for label, (cell, expected) in checks.items():
    try:
        got = v(cell)
    except Exception as exc:  # noqa: BLE001
        fails.append((label, cell, "ERROR " + str(exc)[:80]))
        continue
    if expected is None:
        print("%-22s %-18s %s" % (label, cell, got))
        continue
    if isinstance(expected, str):
        ok = str(got) == expected
        print("%-22s %-18s %-14s expected %s %s" % (label, cell, got, expected, "OK" if ok else "MISMATCH"))
        if not ok:
            fails.append((label, cell, got))
    else:
        diff = abs(float(got) - expected) / max(abs(expected), 1e-9)
        worst = max(worst, diff)
        ok = diff < 0.01
        print("%-22s %-18s %12.4f  expected %12.4f  %s" % (label, cell, float(got), expected, "OK" if ok else "MISMATCH"))
        if not ok:
            fails.append((label, cell, got))

print()
print("worst relative deviation: %.4f%%" % (worst * 100))
print("FAILURES:", len(fails))
for f in fails:
    print("  ", f)
sys.exit(1 if fails else 0)
