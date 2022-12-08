FROM python:3.10
RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt
COPY train_test_split.py /train_test_split.py

ENTRYPOINT ["python", "train_test_split.py"]