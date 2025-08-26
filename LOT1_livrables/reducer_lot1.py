#!/usr/bin/env python3
import sys

sum_qte, ville_nom, timbre = {}, {}, {}

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line or "\t" not in line:
        continue
    k, rest = line.split("\t", 1)
    parts = rest.split(",", 2)  # ville,qte,timbrecde
    if len(parts) != 3:
        continue

    ville = parts[0]
    try: qte = int(float(parts[1]))
    except: qte = 0
    try: tbcde = float(parts[2])
    except: tbcde = 0.0

    sum_qte[k] = sum_qte.get(k, 0) + qte
    if k not in ville_nom and ville:
        ville_nom[k] = ville
    if k not in timbre or tbcde > timbre[k]:
        timbre[k] = tbcde

for k in sum_qte:
    v = ville_nom.get(k, "")
    t = timbre.get(k, 0.0)
    sys.stdout.write(k + "\t" + v + "\t" + str(sum_qte[k]) + "\t" + ("%.2f" % t) + "\n")
