from pydantic import BaseModel, validate_arguments

# @validate_arguments


class InputData(BaseModel):
    name: str  # имя пациента (для идентификации)
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: int
    slope: int
    ca: int
    thal: int
    condition: int = 0
