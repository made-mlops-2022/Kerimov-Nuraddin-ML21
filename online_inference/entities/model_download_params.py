from dataclasses import dataclass, fields
from path import Path


@dataclass
class InferenceDownloadParams:
    model_path: Path = Path('./models')
    model_name: Path = Path('model.pkl')
    file_id: str = None  # '1B1BvfrkKKimI0kTxYVgXwOMG3zHhsptC'
    zip_path: Path = Path('data.zip')
    url: str = 'https://docs.google.com/uc?export=download'

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if (field.type == Path) and not isinstance(value, field.type):
                setattr(self, field.name, field.type(value))
