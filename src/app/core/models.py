import pickle
import wandb
from sklearn.svm import SVC


project = "dsproject"
entity = "double-l-team"


def get_baseline_model():
    
    run = wandb.init(project=project, entity=entity)

    model_file = 'model.pkl' # change this
    artifact_name = 'my-handwritten-recognition' # change this

    art = run.use_artifact(f'{artifact_name}:latest')

    model = art.get_path(model_file).download()
    clf = pickle.load(open(model, 'rb'))

    run.finish()

    return clf


