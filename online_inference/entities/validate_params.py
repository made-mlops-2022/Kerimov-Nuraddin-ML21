from dataclasses import dataclass, fields
from path import Path


@dataclass
class ValidateParams:
    data_path: Path = Path('./train_data')
    data_name: Path = Path('heart_cleveland_upload.csv')
    file_id: str = '1q2ehxJdWkP-ak84wIc6GWRhCC3bgSTC4'
    zip_path: Path = Path('heart_cleveland_upload.csv')
    url: str = 'https://docs.google.com/uc?export=download'

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if (field.type == Path) and not isinstance(value, field.type):
                setattr(self, field.name, field.type(value))
