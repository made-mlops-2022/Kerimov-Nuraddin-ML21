FROM python:3.10
RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt
COPY get_data.py /get_data.py

ENTRYPOINT ["python", "get_data.py"]