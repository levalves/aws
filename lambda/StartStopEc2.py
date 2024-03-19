# ===========================================================================
# Licensed Materials - Property of Levinux
# "Restricted Materials of Levinux"
# 
# Levinux Scripting
# (C) Copyright Levinux. 2023. All Rights Reserved
# ===========================================================================
# Title           : StartStopEc2.py
# Description     : Start and Stop EC2 instances with tag maintenace="yes" or "no"
# Author          : levi.linux@hotmail.com
# Date            : 2023-Dec-13
# Version         : 1.0
# ===========================================================================
# Este script inicia e para instâncias EC2 com base na tag de manutenção

import boto3

def lambda_handler(event, context):
    # Lista de regiões que você deseja controlar
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        
        # Lista todas as instâncias EC2 na região atual
        instances = ec2.describe_instances()
        
        # Verifica o estado e a tag de manutenção de cada instância e toma a ação apropriada
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_state = instance['State']['Name']
                
                print(f"Região: {region}")
                print(f"ID da instância EC2: {instance_id}")
                
                # Verificar se a instância possui a tag 'maintenance' definida como 'yes'
                tags = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [instance_id]}])['Tags']
                maintenance_tag = next((tag for tag in tags if tag['Key'] == 'maintenance'), None)
                
                if maintenance_tag and maintenance_tag['Value'].lower() == 'yes':
                    # A tag "maintenance" está definida como "yes", então executar a ação correspondente
                    if instance_state == 'stopped':
                        try:
                            # Iniciar a instância EC2
                            response = ec2.start_instances(InstanceIds=[instance_id])
                            print(f"Iniciando a instância EC2 {instance_id}. Resposta: {response}")
                        except Exception as e:
                            print(f"Erro ao iniciar a instância {instance_id}: {str(e)}")
                    elif instance_state == 'running':
                        try:
                            # Parar a instância EC2
                            response = ec2.stop_instances(InstanceIds=[instance_id])
                            print(f"Parando a instância EC2 {instance_id}. Resposta: {response}")
                        except Exception as e:
                            print(f"Erro ao parar a instância {instance_id}: {str(e)}")
                    else:
                        print(f"O estado da instância {instance_id} não é suportado ou desconhecido.")
                else:
                    print(f"A instância {instance_id} não está marcada para manutenção (maintenance=no).")
