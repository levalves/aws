# Lambda Function: StartEc2Param.py / StopEc2Param.py

Este script Python é destinado a ser usado como uma função AWS Lambda. Ele verifica as tags de instâncias EC2 em diferentes regiões e faz o start e stop para as instâncias marcadas para manutenção.

### Pré-requisitos

- AWS Lambda configurada para execução do script.
- Permissões adequadas para a função Lambda acessar o serviço EC2.

Policy name:                | Type:
-------------------------   | ---------------
AmazonEC2InstanceStopStart  | Customer managed


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2PowerOnOff",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*"
        }
    ]
}
```

Policy name:                | Type:
-------------------------   | ---------------
AmazonEC2ReadOnlyAccess     | AWS managed

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "elasticloadbalancing:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cloudwatch:ListMetrics",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:Describe*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "autoscaling:Describe*",
            "Resource": "*"
        }
    ]
}
```

Policy name:                                | Type:
-----------------------------------------   | ---------------
AmazonS3ObjectLambdaExecutionRolePolicy     | AWS managed

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3-object-lambda:WriteGetObjectResponse"
            ],
            "Resource": "*"
        }
    ]
}
```

### Parâmetros de Entrada

A função Lambda aceita os seguintes parâmetros através do objeto de evento:

- **regions (opcional):** Lista das regiões AWS a serem verificadas. Padrão: ['sa-east-1'].
- **instance_ids (opcional):** Lista de IDs de instâncias EC2 a serem verificadas. Padrão: ['i-xxxxxxxxxxxxxxxx'].

**Exemplo de Objeto de Evento:**
```json
{
  "regions": ["us-west-2", "eu-central-1"],
  "instance_ids": ["i-xxxxxxxxxxxxxxxx", "i-yyyyyyyyyyyyyyyy"]
}
```
### Funcionamento
1. A função itera sobre as regiões fornecidas.
2. Para cada região, verifica as tags da instância EC2 especificada.
3. Se a tag "maintenance" estiver presente e configurada como "yes", inicia a instância.
4. Registra mensagens de saída informando o resultado do processo.

### Manipulação de Erros
O script trata diferentes cenários de erro, como parâmetros ausentes, falhas ao verificar tags ou iniciar instâncias. Mensagens de erro específicas são registradas para diagnóstico.

### Exemplo de Uso
Este script pode ser invocado através de eventos Lambda ou manualmente para iniciar instâncias EC2 marcadas para manutenção.

### Notas Adicionais
* Certifique-se de configurar corretamente as permissões IAM para a função Lambda.
* Garanta que a função Lambda tenha acesso suficiente para as regiões e instâncias EC2 especificadas.

### Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de pull.

### Licença
Este script é distribuído sob a licença MIT.

---

# Lambda Function: StartEc2Asg.py / StopEc2Asg.py

Este script Python é destinado a ser usado como uma função AWS Lambda. Ele verifica as instâncias EC2 marcadas para manutenção (com a tag 'maintenance=yes') em diferentes regiões e realiza ações correspondentes, como iniciar / parar instâncias ou ajustar configurações de grupos de Auto Scaling.

### Pré-requisitos

- AWS Lambda configurada para execução do script.
- Permissões adequadas para a função Lambda acessar os serviços EC2 e Auto Scaling.

Policy name:                | Type:
-------------------------   | ---------------
AmazonEC2InstanceStopStart  | Customer managed


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2PowerOnOff",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*"
        }
    ]
}
```

Policy name:                | Type:
-------------------------   | ---------------
AmazonEC2ReadOnlyAccess     | AWS managed

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "elasticloadbalancing:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cloudwatch:ListMetrics",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:Describe*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "autoscaling:Describe*",
            "Resource": "*"
        }
    ]
}
```

Policy name:                                | Type:
-----------------------------------------   | ---------------
AmazonS3ObjectLambdaExecutionRolePolicy     | AWS managed

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3-object-lambda:WriteGetObjectResponse"
            ],
            "Resource": "*"
        }
    ]
}
```

### Parâmetros de Entrada

A função Lambda não exige parâmetros específicos de entrada, pois as regiões e outras configurações são definidas diretamente no código. Recomenda-se revisar e ajustar as regiões conforme necessário.

### Funcionamento

O script realiza as seguintes operações:

1. **Iniciar ou Parar instâncias EC2:** Para instâncias marcadas com a tag 'maintenance=yes' que não estão em grupos de Auto Scaling.
2. **Alterar configurações de grupos de Auto Scaling:** Para grupos de Auto Scaling com a tag 'maintenance=yes', altera os valores de MinSize, MaxSize e DesiredCapacity para 1.

### Configuração

Certifique-se de revisar e ajustar as regiões conforme necessário no código.

### Exemplo de Uso

O script pode ser implantado como uma função AWS Lambda. Certifique-se de configurar corretamente as permissões IAM para a função Lambda.

### Notas Adicionais

- Este script é destinado a cenários específicos de manutenção e pode exigir personalização adicional com base nos requisitos específicos.

### Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de pull.

### Licença

Este script é distribuído sob a licença [MIT](LICENSE).

---

# Lambda Function: StartStop-aurora.py

Este script Python é destinado a ser usado como uma função AWS Lambda. Ele controla o estado de clusters de banco de dados Aurora MySQL em diferentes regiões, iniciando ou parando clusters com base nas tags configuradas.

### Pré-requisitos

- AWS Lambda configurada para execução do script.
- Permissões adequadas para a função Lambda acessar o serviço RDS.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RdsPowerOnOff",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "rds:Start*",
                "rds:Stop*",
                "rds:DescribeDBInstances",
                "rds:DescribeDBClusters",
                "rds:ListTagsForResource",
                "autoscaling:UpdateAutoScalingGroup"
            ],
            "Resource": "*"
        }
    ]
}
``` 

### Parâmetros de Entrada

A função Lambda não exige parâmetros específicos de entrada, pois as regiões são definidas diretamente no código. Recomenda-se revisar e ajustar as regiões conforme necessário.

### Funcionamento

O script realiza as seguintes operações:

1. Lista todos os clusters de banco de dados Aurora MySQL na região.
2. Filtra os clusters para incluir apenas aqueles do tipo Aurora MySQL.
3. Verifica o estado de cada cluster e toma a ação apropriada com base nas tags configuradas.
   - Iniciar / Parar clusters marcados para manutenção (`maintenance=yes`) se estiverem parados.

### Configuração

Certifique-se de revisar e ajustar a lista de regiões conforme necessário no código.

### Exemplo de Uso

O script pode ser implantado como uma função AWS Lambda. Certifique-se de configurar corretamente as permissões IAM para a função Lambda.

### Notas Adicionais

- Este script é específico para clusters de banco de dados Aurora MySQL e pode precisar ser adaptado para outros tipos de clusters.
- Verifique se as tags 'maintenance' estão configuradas corretamente nos clusters para controlar o comportamento do script.

### Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de pull.

### Licença

Este script é distribuído sob a licença [MIT](LICENSE).

---

# Lambda Function: StartStopMySQL.py

Este script Python é destinado a ser usado como uma função AWS Lambda. Ele controla o estado de instâncias do banco de dados RDS MySQL Community em diferentes regiões, iniciando ou parando instâncias com base nas tags configuradas.

### Pré-requisitos

- AWS Lambda configurada para execução do script.
- Permissões adequadas para a função Lambda acessar o serviço RDS.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RdsPowerOnOff",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "rds:Start*",
                "rds:Stop*",
                "rds:DescribeDBInstances",
                "rds:DescribeDBClusters",
                "rds:ListTagsForResource",
                "autoscaling:UpdateAutoScalingGroup"
            ],
            "Resource": "*"
        }
    ]
}
``` 

### Parâmetros de Entrada

A função Lambda não exige parâmetros específicos de entrada, pois as regiões são definidas diretamente no código. Recomenda-se revisar e ajustar as regiões conforme necessário.

### Funcionamento

O script realiza as seguintes operações:

1. Lista todas as instâncias RDS MySQL Community na região.
2. Filtra as instâncias para incluir apenas aquelas do tipo MySQL Community.
3. Verifica o estado de cada instância e toma a ação apropriada com base nas tags configuradas.
   - Iniciar / Parar instâncias marcadas para manutenção (`maintenance=yes`) se estiverem paradas.

### Configuração

Certifique-se de revisar e ajustar a lista de regiões conforme necessário no código.

### Exemplo de Uso

O script pode ser implantado como uma função AWS Lambda. Certifique-se de configurar corretamente as permissões IAM para a função Lambda.

### Notas Adicionais

- Este script é específico para instâncias do banco de dados RDS MySQL Community e pode precisar ser adaptado para outros tipos de instâncias.
- Verifique se as tags 'maintenance' estão configuradas corretamente nas instâncias para controlar o comportamento do script.

### Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de pull.

### Licença

Este script é distribuído sob a licença [MIT](LICENSE).

---

# Lambda Function: StartStopPostgreSQL.py

Este script Python é destinado a ser usado como uma função AWS Lambda. Ele controla o estado de instâncias do banco de dados RDS PostgreSQL em diferentes regiões, iniciando ou parando instâncias com base nas tags configuradas.

### Pré-requisitos

- AWS Lambda configurada para execução do script.
- Permissões adequadas para a função Lambda acessar o serviço RDS.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RdsPowerOnOff",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "rds:Start*",
                "rds:Stop*",
                "rds:DescribeDBInstances",
                "rds:DescribeDBClusters",
                "rds:ListTagsForResource",
                "autoscaling:UpdateAutoScalingGroup"
            ],
            "Resource": "*"
        }
    ]
}
``` 

### Parâmetros de Entrada

A função Lambda não exige parâmetros específicos de entrada, pois as regiões são definidas diretamente no código. Recomenda-se revisar e ajustar as regiões conforme necessário.

### Funcionamento

O script realiza as seguintes operações:

1. Lista todas as instâncias RDS PostgreSQL na região.
2. Filtra as instâncias para incluir apenas aquelas do tipo PostgreSQL.
3. Verifica o estado de cada instância e toma a ação apropriada com base nas tags configuradas.
   - Iniciar / Parar instâncias marcadas para manutenção (`maintenance=yes`) se estiverem paradas.

### Configuração

Certifique-se de revisar e ajustar a lista de regiões conforme necessário no código.

### Exemplo de Uso

O script pode ser implantado como uma função AWS Lambda. Certifique-se de configurar corretamente as permissões IAM para a função Lambda.

### Notas Adicionais

- Este script é específico para instâncias do banco de dados RDS PostgreSQL e pode precisar ser adaptado para outros tipos de instâncias.
- Verifique se as tags 'maintenance' estão configuradas corretamente nas instâncias para controlar o comportamento do script.

### Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de pull.

### Licença

Este script é distribuído sob a licença [MIT](LICENSE).

---

# Lambda Function: StartStopEc2.py

Este script Python é destinado a ser usado como uma função AWS Lambda. Ele inicia e para instâncias EC2 com base na tag de manutenção configurada.

## Pré-requisitos

- AWS Lambda configurada para execução do script.
- Permissões adequadas para a função Lambda acessar o serviço EC2.

Policy name:                | Type:
-------------------------   | ---------------
AmazonEC2InstanceStopStart  | Customer managed


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2PowerOnOff",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*"
        }
    ]
}
```

Policy name:                | Type:
-------------------------   | ---------------
AmazonEC2ReadOnlyAccess     | AWS managed

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "elasticloadbalancing:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cloudwatch:ListMetrics",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:Describe*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "autoscaling:Describe*",
            "Resource": "*"
        }
    ]
}
```

Policy name:                                | Type:
-----------------------------------------   | ---------------
AmazonS3ObjectLambdaExecutionRolePolicy     | AWS managed

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3-object-lambda:WriteGetObjectResponse"
            ],
            "Resource": "*"
        }
    ]
}
```

## Parâmetros de Entrada

A função Lambda não exige parâmetros específicos de entrada, pois as regiões são definidas diretamente no código. Recomenda-se revisar e ajustar as regiões conforme necessário.

## Funcionamento

O script realiza as seguintes operações:

1. Lista todas as instâncias EC2 na região.
2. Verifica o estado e a tag de manutenção de cada instância e toma a ação apropriada com base nas tags configuradas.
   - Start das instâncias marcadas para manutenção (`maintenance=yes`) se estiverem paradas.
   - Stop das instâncias marcadas para manutenção (`maintenance=yes`) se estiverem em execução.

## Configuração

Certifique-se de revisar e ajustar a lista de regiões conforme necessário no código.

## Exemplo de Uso

O script pode ser implantado como uma função AWS Lambda. Certifique-se de configurar corretamente as permissões IAM para a função Lambda.

## Notas Adicionais

- Este script controla instâncias EC2 com base em tags configuradas e pode ser adaptado para outras lógicas de controle.
- Verifique se as tags 'maintenance' estão configuradas corretamente nas instâncias para controlar o comportamento do script.

## Licença

Este script é distribuído sob a licença [MIT](LICENSE).

