# ===========================================================================
# Licensed Materials - Property of Levinux
# "Restricted Materials of Levinux"
# 
# Levinux Scripting
# (C) Copyright Levinux. 2023. All Rights Reserved
# ===========================================================================
# Title           : StartStopMySQL.py
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
        
        # Lista todas as instâncias RDS MySQL Community na região atual
        instances = rds.describe_db_instances()
        
        # Filtra as instâncias que são do tipo MySQL Community
        mysql_instances = [
            instance for instance in instances['DBInstances']
            if instance['Engine'] == 'mysql'
        ]
        
        # Verifica o estado de cada instância e toma a ação apropriada
        for instance in mysql_instances:
            db_instance_identifier = instance['DBInstanceIdentifier']
            db_instance_status = instance['DBInstanceStatus']
            
            print(f"Região: {region}")
            print(f"ID da instância RDS MySQL Community: {db_instance_identifier}")
            
            # Verifica as tags da instância
            tags = rds.list_tags_for_resource(ResourceName=instance['DBInstanceArn'])['TagList']
            maintenance_tag = next((tag for tag in tags if tag['Key'] == 'maintenance'), None)
            
            if maintenance_tag and maintenance_tag['Value'].lower() == 'yes':
                # Verificar se a instância está parada
                if db_instance_status == 'stopped':
                    try:
                        # Iniciar a instância RDS MySQL Community
                        response = rds.start_db_instance(DBInstanceIdentifier=db_instance_identifier)
                        print(f"Iniciando a instância RDS MySQL Community {db_instance_identifier}. Resposta: {response}")
                    except Exception as e:
                        print(f"Erro ao iniciar a instância {db_instance_identifier}: {str(e)}")
                # Verificar se a instância está em execução
                elif db_instance_status == 'available':
                    try:
                        # Parar a instância RDS MySQL Community
                        response = rds.stop_db_instance(DBInstanceIdentifier=db_instance_identifier)
                        print(f"Parando a instância RDS MySQL Community {db_instance_identifier}. Resposta: {response}")
                    except Exception as e:
                        print(f"Erro ao parar a instância {db_instance_identifier}: {str(e)}")
                else:
                    print(f"O estado da instância {db_instance_identifier} não é suportado ou desconhecido.")
            else:
                print(f"A instância {db_instance_identifier} não está marcada para manutenção (maintenance=no).")
