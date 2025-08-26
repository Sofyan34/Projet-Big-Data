# 1) Nettoyer un ancien output
hdfs dfs -rm -r -f /user/root/output/lot1

# 2) Lancer le job Hadoop Streaming (sans wrapper)
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
  -D mapreduce.job.name="LOT1 top 100 commandes" \
  -D mapreduce.job.reduces=1 \
  -input  /user/root/dw_data/DW.csv \
  -output /user/root/output/lot1 \
  -mapper  "python3 mapper_lot1.py" \
  -reducer "python3 reducer_lot1.py" \
  -file /root/mapper_lot1.py \
  -file /root/reducer_lot1.py

# 3) Extraire le Top 100 (tri: somme qte desc puis timbrecde desc)
hdfs dfs -cat /user/root/output/lot1/part-* \
  | sort -t$'\t' -k3,3nr -k4,4nr \
  | head -n 100 > /root/lot1_top100.tsv
