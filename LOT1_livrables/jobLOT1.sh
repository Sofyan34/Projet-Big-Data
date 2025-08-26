hdfs dfs -rm -r -f /user/root/output/lot1
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
  -D mapreduce.job.name="LOT1 top 100 commandes" \
  -D mapreduce.job.reduces=1 \
  -input /user/root/dw_data/DW.csv \
  -output /user/root/output/lot1 \
  -mapper "python3 mapper_lot1.py" \
  -reducer "./reduce_lot1.sh" \
  -file /root/mapper_lot1.py \
  -file /root/reducer_lot1.py \
  -file /root/reduce_lot1.sh
# Tri Top100 ensuite
hdfs dfs -cat /user/root/output/lot1/part-* | sort -t$'\t' -k3,3nr -k4,4nr | head -n 100 > /root/lot1_top100.tsv
