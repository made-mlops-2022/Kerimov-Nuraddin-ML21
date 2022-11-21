import requests as r
import pandas as pd
import sys
import os


def main(path: str = None) -> None:
    data = """[
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
]"""

    if path is not None:
        data = pd.read_csv(path)

    resp = r.post('http://127.0.0.1:8000/predict', data)

    print(resp)
    print(resp.text)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            main(sys.argv[1])
        else:
            main()
    else:
        main()
