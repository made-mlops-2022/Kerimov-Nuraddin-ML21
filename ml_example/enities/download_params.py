from dataclasses import dataclass

@dataclass()
class DownloadParams():
    path: str = './data/raw'
    csv: str = 'data.csv'
    file_id: str = '1q2ehxJdWkP-ak84wIc6GWRhCC3bgSTC4'
    zip_path: str = 'data.zip'
    url: str = 'https://docs.google.com/uc?export=download'

