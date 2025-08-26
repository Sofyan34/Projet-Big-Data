#!/usr/bin/env python3
import sys, csv, io

# Lecture robuste UTF-8
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="ignore")
r = csv.reader(sys.stdin, delimiter=",")
first = True

for row in r:
    if not row:
        continue

    # Skip header
    if first:
        first = False
        if row[0].strip().lower() == "codcde":
            continue

    if len(row) < 13:
        continue

    try:
        codcde = row[0].strip()
        datcde = row[1].strip()
        qte_txt = row[4].strip()
        tbcde_txt = row[6].strip()
        ville = row[11].strip()
        dep = row[12].strip()

        year = int(datcde[:4]) if (len(datcde) >= 4 and datcde[:4].isdigit()) else -1
        if not (2006 <= year <= 2010 and dep in {"53","61","28"}):
            continue

        try:
            qte = int(float(qte_txt)) if qte_txt != "" else 0
        except:
            continue
        try:
            tbcde = float(tbcde_txt) if tbcde_txt != "" else 0.0
        except:
            tbcde = 0.0

        if codcde and ville:
            sys.stdout.write(codcde + "\t" + ville + "," + str(qte) + "," + str(tbcde) + "\n")
    except:
        continue
