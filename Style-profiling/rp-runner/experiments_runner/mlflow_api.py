import mlflow

from . import database

mlflow.set_tracking_uri('http://133.186.171.5:5002')

client = mlflow.MlflowClient()


_NAME_MAP = {
    'Wide and Deep': 'wide-deep'
}

def best_model_to_stage():

    models = client.search_model_versions(filter_string='')
    models = [ model for model in models if model.current_stage != 'Production']

    # 
    best_model = sorted(models, key=lambda model:model.tags['rmse'], reverse=True).pop()
    best_model_exp_id = best_model.tags['exp_id']

    current_staging_exp_id = [ model.tags['exp_id'] for model in models if model.current_stage == 'Staging']

    if current_staging_exp_id:
        current_staging_exp_id = current_staging_exp_id.pop()
    else:
        current_staging_exp_id = None

    if current_staging_exp_id == best_model_exp_id:
        pass
    else:
        client.transition_model_version_stage(f'{best_model.name}', best_model.version, 'staging', archive_existing_versions=True)

    database.update_experiment_serving(best_model_exp_id, current_staging_exp_id)



def get_metric(experiment_id):

    filter_string = f"tags.exp_id='{experiment_id}'"

    model = client.search_model_versions(filter_string).pop()
    metric = model.tags['rmse']

    return float(metric)