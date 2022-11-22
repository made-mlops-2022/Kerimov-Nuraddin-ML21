FROM python:3.10.8-slim-buster

COPY requirements_docker.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app

CMD ["uvicorn", "online_inference.server:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
