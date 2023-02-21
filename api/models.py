from enum import Enum, auto
from flask import Response, abort
from http import HTTPStatus
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import CategoricalNB
import logging
from db import persist_model

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

    print(f"Request to create {model_name} with {model_params}")
    # persist in MySQL DB
    unique_id = persist_model(model_name, model_params, model, request_params["d"], request_params["n_classes"], n_trained=0)
    return unique_id
