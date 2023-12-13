# ===========================================================================
# Licensed Materials - Property of Levinux
# "Restricted Materials of Levinux"
# 
# Levinux Scripting
# (C) Copyright Levinux. 2023. All Rights Reserved
# ===========================================================================
# Title           : StartEc2Param.py
# Description     : Start instance EC2 with tag maintenace="yes" or "no"
# Author          : levi.linux@hotmail.com
# Date            : 2023-Dec-13
# Version         : 1.0
# ===========================================================================

import boto3

def lambda_handler(event, context):
    regions = event.get('regions', ['sa-east-1'])
    instance_ids = event.get('instance_ids', ['i-xxxxxxxxxxxxxxxx'])
    
    if not regions or not instance_ids:
        print("Erro: Parâmetros regions e instance_ids são obrigatórios.")
        return
    
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        
        for instance_id in instance_ids:
            try:
                # Verificar as tags da instância
                tags = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [instance_id]}])['Tags']
                maintenance_tag = next((tag for tag in tags if tag['Key'] == 'maintenance'), None)
                
                if maintenance_tag and maintenance_tag['Value'].lower() == 'yes':
                    try:
                        # Iniciar a instância EC2
                        response = ec2.start_instances(InstanceIds=[instance_id])
                        print(f"Iniciando a instância {instance_id} na região {region}. Resposta: {response}")
                    except Exception as e:
                        print(f"Erro ao iniciar a instância {instance_id} na região {region}: {str(e)}")
                else:
                    print(f"A instância {instance_id} deve está em RUNNING, a instância {instance_id} NÃO está marcada para manutenção (maintenance=yes), a instância {instance_id} está com o nome errado ou a instância {instance_id} está em outra região de {region}.")
            except Exception as e:
                print(f"Erro ao verificar as tags da instância {instance_id} na região {region}: {str(e)}")
