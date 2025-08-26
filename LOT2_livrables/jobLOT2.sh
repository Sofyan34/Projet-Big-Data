hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
  -D mapreduce.job.name="LOT2 ami: 2011-2016 dep=22,49,53 timbrecli=0" \
  -D mapreduce.job.reduces=1 \
  -input  /user/root/dw_data/DW.csv \
  -output /user/root/output/lot2 \
  -mapper  "python3 mapper_lot2.py" \
  -reducer "python3 reducer_lot2.py" \
  -file /root/mapper_lot2.py \
  -file /root/reducer_lot2.py


#Ensuite, récupération de la sortie HDFS et la mettre dans /root/out
# (on a 1 seul reducer -> 1 fichier part-00000)
hdfs dfs -get /user/root/output/lot2/part-00000 /root/out/part-00000

# Vérif des résultats
head -n 10 /root/out/part-00000
