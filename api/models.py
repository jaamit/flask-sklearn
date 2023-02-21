from enum import Enum, auto
from flask import Response, abort
from http import HTTPStatus

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

    pass

    