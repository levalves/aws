import boto3

def list_auto_scaling_groups(regions):
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        autoscaling = boto3.client('autoscaling', region_name=region)
        
        # Listar e parar instâncias EC2 com a tag 'maintenance=yes' que não estão em grupos de Auto Scaling
        instances = ec2.describe_instances(Filters=[{'Name': 'tag:maintenance', 'Values': ['yes']}])
        for reservation in instances.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_id = instance['InstanceId']
                try:
                    response = ec2.stop_instances(InstanceIds=[instance_id])
                    print(f"Parando a instância {instance_id} na região {region}. Resposta: {response}")
                except Exception as e:
                    print(f"Não existe instancias a serem paradas na região: {region}. Resposta: {str(e)}")
        
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
                print("A tag 'maintenance' está configurada como 'yes'. Alterando os valores de MinSize, MaxSize e DesiredCapacity para 0.")
                try:
                    autoscaling.update_auto_scaling_group(
                        AutoScalingGroupName=group_name,
                        MinSize=0,
                        MaxSize=0,
                        DesiredCapacity=0
                    )
                    print(f"Valores de MinSize, MaxSize e DesiredCapacity alterados para 0 no grupo {group_name}.")
                except Exception as e:
                    print(f"Erro ao alterar os valores de MinSize, MaxSize e DesiredCapacity no grupo {group_name}: {str(e)}")
            
            print("------")

def lambda_handler(event, context):
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']  # Adicione outras regiões conforme necessário
    list_auto_scaling_groups(regions)

# Uncomment the line below if you are running this script locally
# lambda_handler(None, None)
