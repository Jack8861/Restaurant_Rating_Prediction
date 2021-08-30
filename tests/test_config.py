import pytest
import json
import os
import joblib
from prediction_service.prediction import form_response, api_response
import prediction_service

input_data = {
    "incorrect_range":
        {"votes": -387},
    "correct_range":
        {"votes": 78642},
    "incorrect_col":
        {"vote": 89699}
}

TARGET_RANGE = {
    "min": 0,
    "max": 5
}


def test_form_response_correct_range(data=input_data['correct_range']):
    res = form_response(data)
    assert TARGET_RANGE['min'] <= res <= TARGET_RANGE['max']


def test_api_response_correct_range(data=input_data['correct_range']):
    res = api_response(data)
    assert TARGET_RANGE['min'] <= res["response"] <= TARGET_RANGE['max']


def test_form_response_incorrect_range(data=input_data['incorrect_range']):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)


def test_api_response_incorrect_range(data=input_data['incorrect_range']):
    res = api_response(data)
    assert res['response'] == prediction_service.prediction.NotInRange().message


def test_api_response_incorrect_col(data=input_data['incorrect_col']):
    res = api_response(data)
    assert res['response'] == prediction_service.prediction.NotInCols().message

