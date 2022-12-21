FROM python:3.10
RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt
COPY preprocess.py /preprocess.py

ENTRYPOINT ["python", "preprocess.py"]