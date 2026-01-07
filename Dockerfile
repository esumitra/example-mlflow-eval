FROM ghcr.io/mlflow/mlflow:v3.3.1

RUN pip install --upgrade pip
RUN pip install PyMySQL[rsa] boto3 mlflow[auth]