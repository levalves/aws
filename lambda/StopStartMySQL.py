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