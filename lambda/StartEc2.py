# Parada de EC2 onde setamos todas as regions e na precisa adicionar o Instance ID, mas cuidado porque se a TAG maintenance estiver como Yes vai INICIAR TUDO 
import boto3

def lambda_handler(event, context):
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
        
        for reservation in instances.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_id = instance['InstanceId']
                
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
                    print(f"A instância {instance_id} não está marcada para manutenção (maintenance=yes) ou está em outro estado.")
