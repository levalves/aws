# ===========================================================================
# Licensed Materials - Property of Levinux
# "Restricted Materials of Levinux"
# 
# Levinux Scripting
# (C) Copyright Levinux. 2023. All Rights Reserved
# ===========================================================================
# Title           : StartEc2Asg.py
# Description     : Start instance EC2 with tag maintenace="yes" or "no" using Auto Scaling
# Author          : levi.linux@hotmail.com
# Date            : 2023-Dec-13
# Version         : 1.0
# ===========================================================================
import boto3

def list_auto_scaling_groups(regions):
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        autoscaling = boto3.client('autoscaling', region_name=region)
        
        # Listar e iniciar instâncias EC2 com a tag 'maintenance=yes' que não estão em grupos de Auto Scaling
        instances = ec2.describe_instances(Filters=[{'Name': 'tag:maintenance', 'Values': ['yes']}])
        for reservation in instances.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_id = instance['InstanceId']
                try:
                    response = ec2.start_instances(InstanceIds=[instance_id])
                    print(f"Iniciando a instância {instance_id} na região {region}. Resposta: {response}")
                except Exception as e:
                    print(f"Erro ao iniciar a instância {instance_id} na região {region}: {str(e)}")
        
        # Listar grupos de Auto Scaling e alterar valores de MinSize, MaxSize e DesiredCapacity se a tag 'maintenance=yes' estiver presente
        response = autoscaling.describe_auto_scaling_groups()
        auto_scaling_groups = response['AutoScalingGroups']
        for group in auto_scaling_groups:
            group_name = group['AutoScalingGroupName']
            tags = group['Tags']
            tag_dict = {tag['Key']: tag['Value'] for tag in tags}
            print(f"Região: {region}")
            print(f"Auto Scaling Group Name: {group_name}")
            print(f"Tags: {tag_dict}")
            
            if tag_dict.get('maintenance') == 'yes':
                print("A tag 'maintenance' está configurada como 'yes'. Alterando os valores de MinSize, MaxSize e DesiredCapacity para 1.")
                try:
                    autoscaling.update_auto_scaling_group(
                        AutoScalingGroupName=group_name,
                        MinSize=1,
                        MaxSize=1,
                        DesiredCapacity=1
                    )
                    print(f"Valores de MinSize, MaxSize e DesiredCapacity alterados para 1 no grupo {group_name}.")
                except Exception as e:
                    print(f"Erro ao alterar os valores de MinSize, MaxSize e DesiredCapacity no grupo {group_name}: {str(e)}")
            
            print("------")

def lambda_handler(event, context):
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']  # Adicione outras regiões conforme necessário
    list_auto_scaling_groups(regions)

# Uncomment the line below if you are running this script locally
# lambda_handler(None, None)
