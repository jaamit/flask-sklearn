from enum import Enum, auto
from flask import Response, abort
from http import HTTPStatus
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import CategoricalNB
import logging
from db import persist_model, retrieve_model, update_num_train, retrieve_model_groups
import json
import pickle
import numpy as np

class ClassifierEnum(Enum):
    MLPClassifier = 0
    SGDClassifier = 1
    CategoricalNB = 2
    
def _validate_name(model_name):
    return model_name in ClassifierEnum._member_names_

def create_classifier_model(request_params):
    model_name = request_params["model"]    
    if not _validate_name(model_name=model_name):
        abort(HTTPStatus.BAD_REQUEST, description = "Invalid Model Name")

    model_params = request_params["params"]
    model = None
    if model_name == ClassifierEnum.MLPClassifier.name:
        model = MLPClassifier()
        model.set_params(**model_params)
    elif model_name == ClassifierEnum.SGDClassifier.name:
        model = SGDClassifier()
        model.set_params(**model_params)
    elif model_name == ClassifierEnum.CategoricalNB.name:
        model = CategoricalNB()
        model.set_params(**model_params)
    else:
        # Flexible to add more models. Solution is for 3 models only for the moment 
        abort(HTTPStatus.BAD_REQUEST, description = "Invalid Model Name")

    
    # persist in MySQL DB
    unique_id = persist_model(model_name, model_params, model, request_params["d"], request_params["n_classes"], n_trained=0)
    print(f"Request to create {model_name} with {model_params} id {unique_id}")
    return unique_id

def fetch_model(model_id):
    records = retrieve_model(model_id)
    print("Total rows are: ", len(records), " for model id ", model_id)
    result = {}
    for row in records:
        result['model'] = row[1]
        result['params'] = json.loads(row[2])
        result['d'] = row[4]
        result['n_classes'] = row[5]
        result['n_trained'] = row[6]
    
    return result

def train_the_model(model_id, request_data):
    records = retrieve_model(model_id)
    print("Train_the_model", model_id)
    result = {}
    for row in records:
        result['model'] = row[1]
        result['params'] = json.loads(row[2])
        result['pkl_model'] = pickle.loads(row[3])
        result['d'] = row[4]
        result['n_classes'] = row[5]
        result['n_trained'] = row[6]

    X = [request_data["x"]]
    y = [request_data["y"]]
    y_all = np.arange(result['n_classes'])

    try:
        clf = result['pkl_model'].partial_fit(X, y, classes=(y_all,))
    except:
        abort(HTTPStatus.BAD_REQUEST, description = "Invalid X/y Dimensions")
    update_num_train(model_id, result['n_trained']+1, clf)

def predict_model(model_id, x):
    records = retrieve_model(model_id)
    print("Predict model", model_id)
    result = {}
    for row in records:
        result['model'] = row[1]
        result['params'] = json.loads(row[2])
        result['pkl_model'] = pickle.loads(row[3])
        result['d'] = row[4]
        result['n_classes'] = row[5]
        result['n_trained'] = row[6]

    if len(x) != result['d']:
        abort(HTTPStatus.BAD_REQUEST, description = "Invalid Feature Vector")
    
    y = result['pkl_model'].predict([x])
    print(f'Model Prediction {y} for model_id {model_id}')
    return y

def group_models_by_training_stage():
    return retrieve_model_groups()