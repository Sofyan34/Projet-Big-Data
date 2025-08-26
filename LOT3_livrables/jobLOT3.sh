# Choisir Excel si présent, sinon le CSV de secours
Q3_EXCEL="/root/LOT3_q3_top_client_timbrecde.xlsx"
[ -f "$Q3_EXCEL" ] || Q3_EXCEL="/root/LOT3_q3_top_client_timbrecde.csv"

tar -czf /root/LOT3_livrables.tgz \
  /root/LOT3_q1_best_order_nantes_2020.csv \
  /root/LOT3_q2_counts_2010_2015.csv \
  /root/LOT3_q2_counts_bar.pdf \
  /root/LOT3_q3_top_client_timbrecde.xlsx

echo "OK -> /root/LOT3_livrables.tgz"