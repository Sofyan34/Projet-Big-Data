import csv, random

try:
    src = '/root/out/part-00000'
    with open(src, 'r', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        lines = list(reader)

    # 5 lignes aléatoires (si <5, on prend tout)
    k = 5 if len(lines) >= 5 else len(lines)
    echantillon = random.sample(lines, k)

    dst = '/root/out/sample5.csv'
    with open(dst, 'w', newline='', encoding='utf-8') as csvfile:
        w = csv.writer(csvfile)  # CSV virgules
        w.writerows(echantillon)

    print("OK ->", dst)
except Exception as e:
    print("Erreur:", e)