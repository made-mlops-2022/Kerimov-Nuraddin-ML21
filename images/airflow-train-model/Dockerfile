FROM python:3.10
RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt
COPY train_model.py /train_model.py

ENTRYPOINT ["python", "train_model.py"]