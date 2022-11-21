from fastapi.testclient import TestClient
import json
from online_inference.server import app
import time


def test_predict():
    with TestClient(app) as client:

        response = client.post(
            "/predict/",
            json=json.loads("""[
    {
        "name": "string",
        "age": 35,
        "sex": 1,
        "cp": 3,
        "trestbps": 126,
        "chol": 282,
        "fbs": 0,
        "restecg": 2,
        "thalach": 156,
        "exang": 1,
        "oldpeak": 0,
        "slope": 0,
        "ca": 0,
        "thal": 2
    }
    ]""")

        )
        assert response.status_code == 200
        assert response.json() == {
            "name":["string"],
            "age":[35],
            "sex":[1],
            "cp":[3],
            "trestbps":[126],
            "chol":[282],
            "fbs":[0],
            "restecg":[2],
            "thalach":[156],
            "exang":[1],
            "oldpeak":[0],
            "slope":[0],
            "ca":[0],
            "thal":[2],
            "condition":[1]
            }
        
