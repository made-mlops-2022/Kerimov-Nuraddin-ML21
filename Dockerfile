

FROM python:3.10.8-slim-buster as base
WORKDIR /app
RUN python -m venv /app/venv && /app/venv/bin/pip install --no-cache-dir -U pip setuptools
COPY requirements_docker.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements_docker.txt && /app/venv/bin/pip uninstall -y plotly Pillow matplotlib pip
FROM python:3.10.8-slim-buster
COPY --from=base /app /app
WORKDIR /app
COPY /online_inference /app/online_inference
COPY /configs /app/configs
COPY /ml_example /app/ml_example
CMD ["/app/venv/bin/uvicorn", "online_inference.server:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000

