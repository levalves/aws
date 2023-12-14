# ===========================================================================
# Licensed Materials - Property of Levinux
# "Restricted Materials of Levinux"
# 
# Levinux Scripting
# (C) Copyright Levinux. 2023. All Rights Reserved
# ===========================================================================
# Title           : StartStop-aurora.py
# Description     : Start and Stop instance RDS with tag maintenace="yes" or "no"
# Author          : levi.linux@hotmail.com
# Date            : 2023-Dec-13
# Version         : 1.0
# ===========================================================================
import boto3

def lambda_handler(event, context):
    # Lista de regiões que você deseja controlar
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    
    for region in regions:
        rds = boto3.client('rds', region_name=region)
        
        # Lista todos os clusters de banco de dados Aurora na região atual
        clusters = rds.describe_db_clusters()
        
        # Filtra os clusters que são do tipo Aurora MySQL
        aurora_mysql_clusters = [
            cluster for cluster in clusters['DBClusters']
            if 'aurora' in cluster['Engine'].lower() and 'mysql' in cluster['Engine'].lower()
        ]
        
        # Verifica o estado de cada cluster e toma a ação apropriada
        for cluster in aurora_mysql_clusters:
            db_cluster_identifier = cluster['DBClusterIdentifier']
            db_cluster_status = cluster['Status']
            
            print(f"Região: {region}")
            print(f"ID do cluster Aurora MySQL: {db_cluster_identifier}")
            
            # Verificar as tags do cluster
            tags = rds.list_tags_for_resource(ResourceName=cluster['DBClusterArn'])['TagList']
            maintenance_tag = next((tag for tag in tags if tag['Key'] == 'maintenance'), None)
            
            if maintenance_tag and maintenance_tag['Value'].lower() == 'yes':
                # Verificar se o cluster está parado
                if db_cluster_status == 'stopped':
                    try:
                        # Iniciar o cluster Aurora MySQL
                        response = rds.start_db_cluster(DBClusterIdentifier=db_cluster_identifier)
                        print(f"Iniciando o cluster Aurora MySQL {db_cluster_identifier}. Resposta: {response}")
                    except Exception as e:
                        print(f"Erro ao iniciar o cluster {db_cluster_identifier}: {str(e)}")
                # Verificar se o cluster está em execução
                elif db_cluster_status == 'available':
                    try:
                        # Parar o cluster Aurora MySQL
                        response = rds.stop_db_cluster(DBClusterIdentifier=db_cluster_identifier)
                        print(f"Parando o cluster Aurora MySQL {db_cluster_identifier}. Resposta: {response}")
                    except Exception as e:
                        print(f"Erro ao parar o cluster {db_cluster_identifier}: {str(e)}")
                else:
                    print(f"O estado do cluster {db_cluster_identifier} não é suportado ou desconhecido.")
            else:
                print(f"O cluster {db_cluster_identifier} não está marcado para manutenção (maintenance=no).")
