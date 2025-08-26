import sys, io
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='ignore')

cur = None
ville_kept = ""
qte_tot = 0
n_lines = 0
sum_no_tcli = 0

def flush(cur, ville_kept, qte_tot, n_lines, sum_no_tcli):
    if cur is None:
        return
    avg = (float(qte_tot)/n_lines) if n_lines > 0 else 0.0
    # colonnes : codcde \t ville \t qte_totale \t sum_no_tcli \t avg_qte
    sys.stdout.write("{0}\t{1}\t{2}\t{3}\t{4:.2f}\n".format(cur, ville_kept, qte_tot, sum_no_tcli, avg))

for line in sys.stdin:
    line = line.strip()
    if not line or "\t" not in line:
        continue
    key, payload = line.split("\t", 1)
    try:
        v, q_str, tcli_str = payload.split("|")
    except:
        continue

    try:
        q = int(float(q_str))
    except:
        q = 0

    try:
        tcli = float(tcli_str) if tcli_str != "" else 0.0
    except:
        tcli = 0.0

    if cur is not None and key != cur:
        flush(cur, ville_kept, qte_tot, n_lines, sum_no_tcli)
        qte_tot = 0; n_lines = 0; sum_no_tcli = 0
        ville_kept = ""

    if cur is None or key != cur:
        cur = key

    if not ville_kept and v:
        ville_kept = v

    qte_tot += q
    n_lines += 1
    if tcli == 0.0:
        sum_no_tcli += q

flush(cur, ville_kept, qte_tot, n_lines, sum_no_tcli)