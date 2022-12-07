from mlflow import MlflowClient
import mlflow
import os


mlflow.set_tracking_uri('http://133.186.171.5:5002')
client = MlflowClient()

model_name = 'wide-deep'
results = client.search_model_versions(f"name='{model_name}'")

best_model = sorted(results, key=lambda model:model.tags['rmse'], reverse=False).pop()

client.transition_model_version_stage(f'{model_name}', best_model.version, 'staging')