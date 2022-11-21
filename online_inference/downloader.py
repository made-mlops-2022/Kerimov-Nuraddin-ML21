# -*- coding: utf-8 -*-
import requests as r
import os
# https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url


def download_file_from_google_drive(file_id: str, destination: str, url: str) -> None:
    session = r.Session()

    response = session.get(url, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    print(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)
    # session.close()


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination: str) -> None:
    CHUNK_SIZE = 32768  # hardcode

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
