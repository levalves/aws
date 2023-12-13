# Lambda Function: PowerbiStartEc2.py

Este script Python é destinado a ser usado como uma função AWS Lambda. Ele verifica as tags de instâncias EC2 em diferentes regiões e inicia as instâncias marcadas para manutenção.

## Pré-requisitos

- AWS Lambda configurada para execução do script.
- Permissões adequadas para a função Lambda acessar o serviço EC2.

## Parâmetros de Entrada

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

# Lambda Function: StopEc2Param.py

Este script Python é destinado a ser usado como uma função AWS Lambda. Ele verifica as tags de instâncias EC2 em diferentes regiões e para as instâncias marcadas para manutenção, ele as para.

## Pré-requisitos

- AWS Lambda configurada para execução do script.
- Permissões adequadas para a função Lambda acessar o serviço EC2.

## Parâmetros de Entrada

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
