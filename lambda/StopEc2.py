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
# Parada de EC2 onde setamos todas as regions e na precisa adicionar o Instance ID, mas cuidado porque se a TAG maintenance estiver como Yes vai PARAR TUDO 

import boto3

def lambda_handler(event, context):
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        
        for reservation in instances.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_id = instance['InstanceId']
                
                # Verificar as tags da instância
                tags = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [instance_id]}])['Tags']
                maintenance_tag = next((tag for tag in tags if tag['Key'] == 'maintenance'), None)
                
                if maintenance_tag and maintenance_tag['Value'].lower() == 'yes':
                    try:
                        # Parar a instância EC2
                        response = ec2.stop_instances(InstanceIds=[instance_id])
                        print(f"Parando a instância {instance_id} na região {region}. Resposta: {response}")
                    except Exception as e:
                        print(f"Erro ao parar a instância {instance_id} na região {region}: {str(e)}")
                else:
                    print(f"A instância {instance_id} NÂO está marcada para manutenção (maintenance=yes) ou está em outro estado.")
