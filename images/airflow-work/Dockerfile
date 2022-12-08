FROM python:3.10
RUN mkdir /build/
COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt
COPY work.py /work.py

ENTRYPOINT ["python", "work.py"]