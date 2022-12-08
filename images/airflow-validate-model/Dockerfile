FROM python:3.10
RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt
COPY validate_model.py /validate_model.py

ENTRYPOINT ["python", "validate_model.py"]