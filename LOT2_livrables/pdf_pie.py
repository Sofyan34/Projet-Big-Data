import io, collections
try:
    import matplotlib # type: ignore
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt # type: ignore
except:
    raise SystemExit("Installe matplotlib: pip3 install 'matplotlib<3.0'")

villes = []
for l in io.open("/root/LIVRABLES/LOT2/lot2_top100.tsv","r",encoding="utf-8",errors="ignore"):
    p = l.strip().split("\t")
    if len(p) >= 2:
        villes.append(p[1])

c = collections.Counter(villes)
labels, values = list(c.keys()), list(c.values())
fig = plt.figure()
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title("LOT2 – Répartition des TOP100 par ville")
plt.tight_layout()
plt.savefig("/root/LIVRABLES/LOT2/LOT2_pie.pdf", bbox_inches="tight")
plt.close(fig)
print("OK -> /root/LIVRABLES/LOT2/LOT2_pie.pdf")