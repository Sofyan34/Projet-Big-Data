import sys, csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for row in reader:
    # ignorer lignes vides / incomplètes
    if not row or len(row) < 13:
        continue
    # dépaquetage (13 colonnes attendues)
    codcde, datcde, codobj, libobj, qte, timbrecli, timbrecde, codcli, nomcli, prenomcli, cpcli, ville, departement = row

    # champs vitaux
    if not datcde or not departement or not qte:
        continue
    try:
        year = int(datcde[:4])          # année
        dep  = int(departement)         # département (22/49/53)
        q    = int(qte)                 # quantité
        tb_cde = float(timbrecde)       # timbrecde (pour tri secondaire)
        tb_cli = float(timbrecli)       # timbrecli (filtre == 0.0)
    except Exception:
        continue

    if (2011 <= year <= 2016) and (dep in (22, 49, 53)) and (tb_cli == 0.0):
        # sortie: codcde, qte, timbrecde, timbrecli, ville
        sys.stdout.write("%s\t%s\t%s\t%s\t%s\n" % (codcde, q, tb_cde, tb_cli, ville))