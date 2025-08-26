import sys

current_cde = None
current_ville = None
qte_tot = 0
n_lines = 1
sans_timbrecli = 0  # ici = qte_tot car mapper filtre timbrecli==0
result = []

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) < 5:
        continue
    codcde_s, qte_s, timbrecde_s, timbrecli_s, ville_s = parts
    try:
        codcde = int(codcde_s.strip())
        qte = int(qte_s.strip())
        timbrecde = float(timbrecde_s.strip())
        # timbrecli = float(timbrecli_s.strip())  # toujours 0.0 ici
        ville = ville_s.strip()
    except Exception:
        continue

    if current_cde == codcde:
        qte_tot += qte
        sans_timbrecli += qte
        n_lines += 1
    else:
        if current_cde is not None:
            q_avg = round(qte_tot / float(n_lines), 2)
            # garder timbrecde juste comme critère secondaire (dernier vu)
            result.append([current_cde, qte_tot, timbrecde, current_ville, sans_timbrecli, q_avg])
        current_cde = codcde
        current_ville = ville
        qte_tot = qte
        n_lines = 1
        sans_timbrecli = qte

# dernière commande
if current_cde is not None:
    q_avg = round(qte_tot / float(n_lines), 2)
    result.append([current_cde, qte_tot, timbrecde, current_ville, sans_timbrecli, q_avg])

# tri: total qte desc puis timbrecde desc
result.sort(key=lambda e: (e[1], e[2]), reverse=True)

# top 100
result = result[:100] if len(result) >= 100 else result

# sortie TSV: cde \t ville \t qte_sans_timbre \t qt_avg
for ele in result:
    sys.stdout.write("%d\t%s\t%d\t%.2f\n" % (ele[0], ele[3], ele[4], ele[5]))