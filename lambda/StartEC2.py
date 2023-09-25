import boto3

def lambda_handler(event, context):
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
        
        stopped_instance_ids = [instance['InstanceId'] for reservation in instances.get('Reservations', []) for instance in reservation.get('Instances', [])]
        
        print("Região:", region)
        print("IDs das instâncias paradas:", stopped_instance_ids)
        
        if stopped_instance_ids:
            response = ec2.start_instances(InstanceIds=stopped_instance_ids)
            print(f"Iniciando instâncias na região {region}. Resposta: {response}")