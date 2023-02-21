from enum import Enum, auto
from flask import Response, abort
from http import HTTPStatus
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier
# from sklearn.naive_bayes import CategoricalNB
import logging


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class ClassifierEnum(AutoName):
    MLPClassifier = auto()
    SGDClassifier = auto()
    CategoricalNB = auto()

    def equals(self, model_name):
        return self.name == model_name
    
def _validate_name(model_name):
    return model_name in list(ClassifierEnum)

def create_classifier_model(request_params):
    model_name = request_params["model"]
    if not _validate_name(model_name=model_name):
        abort(HTTPStatus.BAD_REQUEST, description = "Invalid Model Name")

    # model_params = request_params["params"]
    # logging.DEBUG(model_params)
    # if model_name == ClassifierEnum.MLPClassifier:
    #     pass
    # elif model_name == ClassifierEnum.SGDClassifier:
    #     # model = SGDClassifier(**model_params)
    #     model = SGDClassifier()
    #     print(model)
    #     pass
    # else:
    #     pass
    # pass

    