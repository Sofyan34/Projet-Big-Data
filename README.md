#1 : Démarrage de la VM et lancement d'Hadoop
# Démarrer la VM avec Putty, se connecter à sa machine attribuée et se connecter (login : root, mdp indiqué)

# Lister les conteneurs en cours d’exécution :
docker ps

# Démarrage du contenur 
./start_docker_digi.sh

# Entrer dans le conteneur hadoop-master :
./bash_hadoop_master.sh

# Lancement des serveurs Slaves
./lance_srv_slaves.sh

# Quitter le conteneur si besoin 
exit

#2 : Transférer le fichier CSV vers la VM (FileZilla)

# Connexion au serveur via protocole SFTP

# Déplacer le fichier dans le conteneur Hadoop : /!\ à executer dans la VM HORS du conteneur
docker cp /root/DW.csv hadoop-master:/root/DW.csv
# Vérifier une fois dans le conteneur 
docker exec -it hadoop-master ls /root

# Charger le fichier CSV dans HDFS
hdfs dfs -mkdir -p /user/root/dw_data
hdfs dfs -put /root/DW.csv /user/root/dw_data/
hdfs dfs -ls /user/root/dw_data

#3 Executer le job Hadoop Streaming voulu 
