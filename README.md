# Configuration technique

## 1. Langages et versions

Python 3.5.2 <br>
GNU bash, version 4.3.48(1) <br>
Hadoop 2.7.2 <br>
HBase 1.4.9 <br>
Microsoft Power BI Desktop 2.146.1133.0 (août 2025)

## 2. Frameworks et bibliothèques

Les libs Python déjà listées dans requirements.txt <br>
API : HappyBase pour interaction HBase <br>
Connecteurs : ODBC HBase driver version 10.0.26100.1150) <br>

## 3. Infra et environnement

VM Linux : AlmaLinux 8.7 <br>
CPU : 13 <br>
RAM : 10 Go <br>
Stockage : 50Go <br>
Ports ouverts :
- SSH : 22
- HBase Thrift → 9090
- HBase REST → 9070
- HBase Master UI → 16010
- YARN ResourceManager → 8088
- Spark Master → 7077
- Spark Worker → 8040 / 8041

## 4. Outils utilisés

IDE : VSCode et Jupyter Notebook <br>
Github et Git <br>
Power BI Desktop ( via ODBC) <br>
Excel et Adobe Acrobat pour les rapports <br>
Google Slides <br>

# Méthode de déploiement

## 1 : Démarrage de la VM et lancement d'Hadoop

- Démarrer la VM avec Putty, se connecter à sa machine attribuée et se connecter (login : root, mdp indiqué)
- Lister les conteneurs en cours d’exécution :
```bash
docker ps
```
- Démarrage du contenur 
```bash
./start_docker_digi.sh
```
- Entrer dans le conteneur hadoop-master :
```bash
./bash_hadoop_master.sh
```
- Lancement des serveurs Slaves
```bash
./lance_srv_slaves.sh
```
- Quitter le conteneur si besoin 
```bash
exit
```

## 2 : Transférer le fichier CSV vers la VM (FileZilla)

- Connexion au serveur via protocole SFTP
- Déplacer le fichier dans le conteneur Hadoop : /!\ à executer dans la VM HORS du conteneur
```bash
docker cp /root/DW.csv hadoop-master:/root/DW.csv
```
- Vérifier une fois dans le conteneur 
```bash
docker exec -it hadoop-master ls /root
```
- Charger le fichier CSV dans HDFS
```bash
hdfs dfs -mkdir -p /user/root/dw_data
hdfs dfs -put /root/DW.csv /user/root/dw_data/
hdfs dfs -ls /user/root/dw_data
```
- Executer le job Hadoop Streaming voulu 
