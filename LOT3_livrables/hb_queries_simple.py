import io, sys

# I/O robustes
sys.stdin  = io.TextIOWrapper(sys.stdin.buffer,  encoding='utf-8', errors='ignore')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

# ---- imports ----
try:
    import happybase # type: ignore
except ImportError:
    sys.stderr.write("HappyBase manquant. Faites: pip3 install happybase thrift\n"); sys.exit(1)
try:
    import pandas as pd
except ImportError:
    sys.stderr.write("pandas manquant. Faites: pip3 install pandas\n"); sys.exit(1)

# Matplotlib optionnel (PDF Q2)
plt = None
try:
    import matplotlib # type: ignore
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt # type: ignore
except Exception as e:
    sys.stderr.write("matplotlib indisponible (PDF Q2 ignoré) : %s\n" % e)

# ---- connexion HBase ----
conn = happybase.Connection('localhost', 9090)
t = conn.table('fromagerie_dw')

# ---- Scan des colonnes utiles -> DataFrame ----
rows = []
cols = [b'commande:datcde', b'commande:qte', b'commande:timbrecde',
        b'client:codcli', b'client:nom', b'client:prenom',
        b'localisation:ville']
for rk, data in t.scan(columns=cols, batch_size=1000):
    key = rk.decode('utf-8')
    codcde = key.split('#', 1)[0]

    datcde = data.get(b'commande:datcde', b'').decode('utf-8')
    qte_s  = data.get(b'commande:qte', b'0').decode('utf-8').replace(',', '.')
    tim_s  = data.get(b'commande:timbrecde', b'0').decode('utf-8').replace(',', '.')
    codcli = data.get(b'client:codcli', b'').decode('utf-8')
    nom    = data.get(b'client:nom', b'').decode('utf-8')
    prenom = data.get(b'client:prenom', b'').decode('utf-8')
    ville  = data.get(b'localisation:ville', b'').decode('utf-8')

    try:
        qte = int(float(qte_s)) if qte_s != "" else 0
    except:
        qte = 0
    try:
        tim = float(tim_s) if tim_s != "" else 0.0
    except:
        tim = 0.0
    try:
        year = int(datcde[:4]) if len(datcde) >= 4 and datcde[:4].isdigit() else None
    except:
        year = None

    rows.append({
        "codcde": codcde, "year": year, "qte": qte, "timbrecde": tim,
        "codcli": codcli, "nom": nom, "prenom": prenom, "ville": ville
    })

if not rows:
    sys.stderr.write("Aucune donnée lue depuis HBase (table fromagerie_dw ? thrift 9090 ?)\n")
    sys.exit(2)

import pandas as pd
df = pd.DataFrame(rows)

# ---- 1 ligne / commande ----
agg = {
    "qte": "sum",
    "timbrecde": "max",
    "year": "first",
    "codcli": "first",
    "nom": "first",
    "prenom": "first",
    "ville": "first"
}
orders = df.groupby("codcde", as_index=False).agg(agg).rename(
    columns={"qte": "sum_qte", "timbrecde": "timbrecde_ord"}
)

# ========= Q1 : meilleure commande Nantes 2020 =========
q1 = orders[(orders["year"] == 2020) & (orders["ville"].str.upper() == "NANTES")]
q1 = q1.sort_values(["sum_qte", "timbrecde_ord"], ascending=[False, False]).head(1)
q1_out = "/root/LOT3_q1_best_order_nantes_2020.csv"
q1_to_write = q1[["codcde","ville","sum_qte","timbrecde_ord"]].rename(columns={"timbrecde_ord":"timbrecde"})
if q1_to_write.empty:
    pd.DataFrame(columns=["codcde","ville","sum_qte","timbrecde"]).to_csv(q1_out, index=False)
else:
    q1_to_write.to_csv(q1_out, index=False)

# ========= Q2 : nb de commandes 2010–2015 =========
q2 = orders[(orders["year"] >= 2010) & (orders["year"] <= 2015)].copy()
q2_counts = q2.groupby("year").size().to_frame("count_cmds").reset_index()
q2_csv = "/root/LOT3_q2_counts_2010_2015.csv"
q2_counts.sort_values("year").to_csv(q2_csv, index=False)

# PDF barplot si matplotlib dispo
try:
    if plt is not None:
        fig = plt.figure()
        xs = [str(int(y)) for y in q2_counts["year"].tolist()]
        ys = [int(c) for c in q2_counts["count_cmds"].tolist()]
        plt.bar(xs, ys)
        plt.title("Nombre de commandes par annee (2010-2015)")
        plt.xlabel("Annee"); plt.ylabel("Nombre de commandes")
        plt.tight_layout()
        plt.savefig("/root/LOT3_q2_counts_bar.pdf", bbox_inches="tight")
        plt.close(fig)
except Exception as e:
    sys.stderr.write("Impossible d'écrire le PDF Q2 : %s\n" % e)

# ========= Q3 : client avec le plus de frais timbrecde =========
clients = orders.groupby(["codcli","nom","prenom"], as_index=False).agg({
    "codcde": "count",
    "sum_qte": "sum",
    "timbrecde_ord": "sum"
}).rename(columns={"codcde":"nb_cmds", "timbrecde_ord":"sum_timbre"})
clients = clients.sort_values("sum_timbre", ascending=False)

# Excel (xlsxwriter requis). Sinon, CSV fallback.
q3_xlsx = "/root/LOT3_q3_top_client_timbrecde.xlsx"
wrote_excel = False
try:
    import xlsxwriter  # type: ignore # noqa
    with pd.ExcelWriter(q3_xlsx, engine="xlsxwriter") as w:
        clients.to_excel(w, index=False, sheet_name="clients_sorted")
        if not clients.empty:
            clients.head(1).to_excel(w, index=False, sheet_name="winner")
    wrote_excel = True
except Exception as e:
    sys.stderr.write("Excel indisponible (xlsxwriter?) : %s\n" % e)

clients.to_csv("/root/LOT3_q3_top_client_timbrecde.csv", index=False)

conn.close()
print("OK -> %s | %s (+PDF si possible) | %s" % (
    q1_out, q2_csv, (q3_xlsx if wrote_excel else "/root/LOT3_q3_top_client_timbrecde.csv")
))