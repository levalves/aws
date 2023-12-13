import boto3

def lambda_handler(event, context):
    # Lista de regiões que você deseja controlar
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    
    for region in regions:
        rds = boto3.client('rds', region_name=region)
        
        # Lista todas as instâncias RDS PostgreSQL na região atual
        instances = rds.describe_db_instances()
        
        # Filtra as instâncias que são do tipo PostgreSQL
        postgres_instances = [
            instance for instance in instances['DBInstances']
            if instance['Engine'] == 'postgres'
        ]
        
        # Verifica o estado e a tag de manutenção de cada instância e toma a ação apropriada
        for instance in postgres_instances:
            db_instance_identifier = instance['DBInstanceIdentifier']
            db_instance_status = instance['DBInstanceStatus']
            
            print(f"Região: {region}")
            print(f"ID da instância RDS PostgreSQL: {db_instance_identifier}")
            
            # Verificar se a instância possui a tag 'maintenance' definida como 'yes'
            tags = rds.list_tags_for_resource(ResourceName=instance['DBInstanceArn'])['TagList']
            maintenance_tag = next((tag for tag in tags if tag['Key'] == 'maintenance'), None)
            
            if maintenance_tag and maintenance_tag['Value'].lower() == 'yes':
                # A tag "maintenance" está definida como "yes", então executar a ação correspondente
                if db_instance_status == 'stopped':
                    try:
                        # Iniciar a instância RDS PostgreSQL
                        response = rds.start_db_instance(DBInstanceIdentifier=db_instance_identifier)
                        print(f"Iniciando a instância RDS PostgreSQL {db_instance_identifier}. Resposta: {response}")
                    except Exception as e:
                        print(f"Erro ao iniciar a instância {db_instance_identifier}: {str(e)}")
                elif db_instance_status == 'available':
                    try:
                        # Parar a instância RDS PostgreSQL
                        response = rds.stop_db_instance(DBInstanceIdentifier=db_instance_identifier)
                        print(f"Parando a instância RDS PostgreSQL {db_instance_identifier}. Resposta: {response}")
                    except Exception as e:
                        print(f"Erro ao parar a instância {db_instance_identifier}: {str(e)}")
                else:
                    print(f"O estado da instância {db_instance_identifier} não é suportado ou desconhecido.")
            else:
                print(f"A instância {db_instance_identifier} não está marcada para manutenção (maintenance=no).")