import os, io, csv, sys
try:
    import happybase # type: ignore
except ImportError:
    sys.stderr.write("HappyBase manquant. Faites: pip3 install happybase thrift\n"); sys.exit(1)

# Connexion Thrift (VM locale)
conn = happybase.Connection('localhost', 9090, autoconnect=False)
conn.open()

TABLE = 'fromagerie_dw'
# Créer la table si besoin
existing = [t.decode('utf-8') if isinstance(t, bytes) else t for t in conn.tables()]
if TABLE not in existing:
    conn.create_table(TABLE, {
        'commande': dict(),
        'client': dict(),
        'localisation': dict(),
    })

table = conn.table(TABLE)

# CSV côté VM
csv_path = '/root/DW.csv'
if not os.path.exists(csv_path):
    csv_path = 'DW.csv'

i = 0
batch = table.batch(batch_size=1000)
with io.open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    r = csv.DictReader(f)
    for row in r:
        i += 1
        # cle de ligne = codcde#000001 (pour de-duplic et tri)
        rk = (row['codcde'] + '#' + ('%06d' % i)).encode('utf-8')
        put = {
            b'commande:codcde':    (row.get('codcde','') or '').encode('utf-8'),
            b'commande:datcde':    (row.get('datcde','') or '').encode('utf-8'),
            b'commande:codobj':    (row.get('codobj','') or '').encode('utf-8'),
            b'commande:libobj':    (row.get('libobj','') or '').encode('utf-8'),
            b'commande:qte':       (row.get('qte','0') or '0').encode('utf-8'),
            b'commande:timbrecli': (row.get('timbrecli','0') or '0').encode('utf-8'),
            b'commande:timbrecde': (row.get('timbrecde','0') or '0').encode('utf-8'),
            b'client:codcli':      (row.get('codcli','') or '').encode('utf-8'),
            b'client:nom':         (row.get('nomcli','') or '').encode('utf-8'),
            b'client:prenom':      (row.get('prenomcli','') or '').encode('utf-8'),
            b'localisation:cp':    (row.get('cpcli','') or '').encode('utf-8'),
            b'localisation:ville': (row.get('villecli','') or '').encode('utf-8'),
            b'localisation:DEP':   (row.get('DEP','') or '').encode('utf-8'),
        }
        batch.put(rk, put)
batch.send()
conn.close()
print("OK: chargement terminé dans 'fromagerie_dw'")

