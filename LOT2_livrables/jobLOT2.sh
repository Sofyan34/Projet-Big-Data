hdfs dfs -rm -r -f /user/root/output/lot2

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
  -D mapreduce.job.name="LOT2 (2011-2016 dep 22/49/53) total + sum_no_tcli + avg" \
  -D mapreduce.job.reduces=1 \
  -input  /user/root/dw_data/DW.csv \
  -output /user/root/output/lot2 \
  -mapper  "python3 mapper_lot2.py" \
  -reducer "python3 reducer_lot2.py" \
  -file /root/mapper_lot2.py \
  -file /root/reducer_lot2.py

#TOP 100 (tri sur qte_totale, puis avg_qte)
hdfs dfs -cat /user/root/output/lot2/part-* \
  | sort -t$'\t' -k3,3nr -k5,5nr \
  | head -n 100 > /root/LIVRABLES/LOT2/lot2_top100.tsv

#Échantillon aléatoire 5% (sur les 100)
python3 - <<'PY'
import random, io
random.seed(42)
p = "/root/LIVRABLES/LOT2/lot2_top100.tsv"
lines = [l for l in io.open(p,"r",encoding="utf-8",errors="ignore") if l.strip()]
sample = random.sample(lines, min(5, len(lines)))
io.open("/root/LIVRABLES/LOT2/lot2_sample5.tsv","w",encoding="utf-8").writelines(sample)
print("OK -> /root/LIVRABLES/LOT2/lot2_sample5.tsv")
PY
