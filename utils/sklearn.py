import time
import os
import joblib

from utils import general


def train_model(classifier,
                train_features,
                train_labels,
                val_features,
                val_labels):
    """
    Training model on the train set and,
    Validate the model on the validation set
    """
    start_time = time.time()

    classifier.fit(train_features, train_labels)

    time_fit = time.time() - start_time

    print(f'Time to train {time_fit} second(s)')


    val_pred_label = classifier.predict(val_features)

    f1_score, cfmatrix = general.get_eval_metrics(val_pred_label, val_labels)

    return time_fit, f1_score, cfmatrix

def save_model_sklearn(model, file_path):
    """
    Save skicit_learn model
    """

    dir_path = os.path.dirname(file_path)

    os.makedirs(dir_path, exist_ok=True)

    joblib.dump(model, file_path)          # dump to joblib file

    print(f"Save model pickle to {file_path}...")


def load_model_sklearn(file_path):
    """
    Save scikit_learn model
    return scikit_learn model
    """

    if not os.path.exists(file_path):
        print(f"There is no {file_path}")

    model = joblib.load(file_path)

    return model


def inference_sklearn(file_path, x_raw_test):
    """
    load the model and predict the raw data test: one instance, return model and prediction label
    """
    model = load_model_sklearn(file_path)

    prediction = model.predict(x_raw_test)

    return prediction


def get_evaluation_on_test_set(file_path, x_test, y_test):

    start_inference_time = time.time()

    pred_label = inference_sklearn(file_path, x_test)

    inference_time = time.time() - start_inference_time

    f1_score, cfmatrix = general.get_eval_metrics(pred_label, y_test)

    return inference_time, f1_score, cfmatrix
