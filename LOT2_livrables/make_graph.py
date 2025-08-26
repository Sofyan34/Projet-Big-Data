import pandas as pd
import matplotlib # type: ignore
matplotlib.use('Agg')
import matplotlib.pyplot as plt # type: ignore

try:
    df = pd.read_csv('/root/out/sample5.csv', header=None).reset_index(drop=True)
    # colonnes depuis le reducer: cde, ville, qte_sans_timbre, qt_avg
    df.columns = ['cde','ville','qte','avg']
    df['qte'] = pd.to_numeric(df['qte'], errors='coerce').fillna(0)

    labels = df['ville'].astype(str).tolist()
    sizes  = df['qte'].astype(float).tolist()

    plt.figure(figsize=(8,6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("5 lignes aléatoires du Top 100 (timbrecli=0)\nSomme des quantités sans timbrecli, par ville")
    plt.axis('equal')
    out = '/root/out/graph.pdf'
    plt.savefig(out, bbox_inches='tight')
    print("OK ->", out)
except Exception as e:
    print("Erreur:", e)