import boto3

def lambda_handler(event, context):
    # Lista de regiões que você deseja controlar
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        
        # Lista todas as instâncias na região atual
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}])
        
        # Extrai as IDs das instâncias
        instance_ids = [instance['InstanceId'] for reservation in instances.get('Reservations', []) for instance in reservation.get('Instances', [])]
        
        print("Região:", region)
        print("IDs das instâncias:", instance_ids)
        
        # Verifica se há instâncias antes de tentar controlar
        if instance_ids:
            # Obtém o estado atual das instâncias (running ou stopped)
            instance_states = ec2.describe_instance_status(InstanceIds=instance_ids)
            
            # Controla as instâncias com base no estado atual
            for instance_state in instance_states['InstanceStatuses']:
                instance_id = instance_state['InstanceId']
                current_state = instance_state['InstanceState']['Name']
                
                if current_state == 'running':
                    # Desligar instância em execução
                    response = ec2.stop_instances(InstanceIds=[instance_id])
                    print(f"Desligando a instância {instance_id} na região {region}. Resposta: {response}")
                elif current_state == 'stopped':
                    # Ligar instância parada
                    response = ec2.start_instances(InstanceIds=[instance_id])
                    print(f"Ligando a instância {instance_id} na região {region}. Resposta: {response}")
