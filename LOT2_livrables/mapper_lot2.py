import sys, csv, io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="ignore")
r = csv.reader(sys.stdin, delimiter=",")
first = True

for row in r:
    if not row:
        continue
    if first:
        first = False
        if row[0].strip().lower() == "codcde":
            continue
    if len(row) < 13:
        continue

    codcde = row[0].strip()
    datcde = row[1].strip()
    qte_txt = row[4].strip().replace(",", ".")
    tcli_txt = row[5].strip().replace(",", ".")
    ville   = row[11].strip()
    dep     = row[12].strip()

    year = int(datcde[:4]) if (len(datcde) >= 4 and datcde[:4].isdigit()) else -1
    if not (2011 <= year <= 2016 and dep in ("22","49","53")):
        continue

    try:
        qte = int(float(qte_txt)) if qte_txt != "" else 0
    except:
        continue

    # clé = codcde ; valeur = ville|qte|timbrecli
    sys.stdout.write("{0}\t{1}|{2}|{3}\n".format(codcde, ville, qte, tcli_txt))