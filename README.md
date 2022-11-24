# HW2 for MLops By Kerimov  Nuraddin

Модель скачивается с гугл диска. Для скачивания с гугл диска нужно передать в переменную окружения ID файла. 
MLOPS_HW2_MODEL_FILE_ID='1B1BvfrkKKimI0kTxYVgXwOMG3zHhsptC'

Валидация входных данных происходит при помощи: определения порядка столбцов, проверка, не выходят ли входные данные за границы данных при обучении и с помощью изолированного леса.


### Установка переменной окружения:
~~~
set MLOPS_HW2_MODEL_FILE_ID='1B1BvfrkKKimI0kTxYVgXwOMG3zHhsptC'
Для Powershell
$Env:MLOPS_HW2_MODEL_FILE_ID = "1B1BvfrkKKimI0kTxYVgXwOMG3zHhsptC" 
~~~

### Запуск сервера с репозитория:
~~~
uvicorn online_inference.server:app --reload
~~~

При переходе в localhost:8000 будет сообщение о дз и об авторе
При переходе в localhost:8000/health будет соответствующий код ошибки и True, если сервер готов
/predict принимает List[Dict] формата, который возвращает pandas при .to_csv('records')
Для удобства была введена колонка name,позволяющая "идентифицировать" пациента

Для проверки теста есть скрипт online_inference.client ,который либо принимает файл и отправляет его, либо (если файл не задан)
отправляет заранее захардкоженную строку

### Запуск скрипта (захардкоженные данные):
~~~
python -m online_inference.client
~~~

### Создание фейковых данных
~~~
python -m ml_example.data.make_dataset путь_выхода количество_объектов

python -m ml_example.data.make_dataset fake_data.csv 1000
~~~

### Запуск скрипта с данными:
~~~
python -m online_inference.client fake_data.csv
~~~

### Запуск теста:
~~~
pytest
~~~

## Докер

### Сборка
~~~
docker build --no-cache -t kaizernurik/hw2mlops .
~~~

### Запуск
~~~
docker run -e MLOPS_HW2_MODEL_FILE_ID='1B1BvfrkKKimI0kTxYVgXwOMG3zHhsptC'  --name kaizernurikhw2mlops -p 8000:8000 kaizernurik/hw2mlops
~~~

### Pull 
~~~
docker pull kaizernurik/hw2mlops
~~~

### Оптимизация данных

Для анализа была использована утилита Dive https://github.com/wagoodman/dive

#### Первая версия Dockerfile (файл Docker #1)
Вес составлял 1.2 Gb, не смотря на slim версию python докера
~~~
FROM python:3.10.8-slim-buster

COPY requirements_docker.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY ./online_inference /opt/app/online_inference

CMD ["uvicorn", "online_inference.server:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
~~~

![](/docs/Docker%231.png)


#### Вторая версия Dockerfile (файл Docker #2)
Для уменьшения размера была использована многоступенчатая сборка
вес 941Мб, выигрыш 250Мб
~~~
FROM python:3.10.8-slim-buster as base
WORKDIR /app
RUN python -m venv /app/venv && /app/venv/bin/pip install --no-cache-dir -U pip setuptools
COPY requirements_docker.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements_docker.txt 

FROM python:3.10.8-slim-buster
COPY --from=base /app /app
WORKDIR /app
COPY /online_inference /app/online_inference
COPY /configs /app/configs
COPY /ml_example /app/ml_example
CMD ["/app/venv/bin/uvicorn", "online_inference.server:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
~~~

![](/docs/Docker%232.png)

#### Вторая версия Dockerfile (файл Dockerfile)
Для последущего уменьшения размера были удалены неиспользованные зависимости библиотек(Графические, которые были не нужны и занимали много места. Также удалён pip)
Размер 592Мб, выигрыш в 600Мб (в 2 раза уменьшилось)
~~~
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
~~~

![](/docs/Docker%233.png)


Основная часть:

    ✅Оберните inference вашей модели в rest сервис на FastAPI, должен быть endpoint /predict (3 балла)

    ✅Напишите endpoint /health, который должен возращать 200, если ваша модель готова к работе (такой чек особенно актуален, если делаете доп задание про скачивание из хранилища) (1 балл)

    ✅Напишите unit тест для /predict (https://fastapi.tiangolo.com/tutorial/testing/, https://flask.palletsprojects.com/en/1.1.x/testing/) (3 балла)

    ✅Напишите скрипт, который будет делать запросы к вашему сервису (2 балла)

    ✅Напишите Dockerfile, соберите на его основе образ и запустите локально контейнер (docker build, docker run). Внутри контейнера должен запускаться сервис, написанный в предущем пункте. Закоммитьте его, напишите в README.md корректную команду сборки (4 балла)

    ✅Опубликуйте образ в https://hub.docker.com/, используя docker push (вам потребуется зарегистрироваться) (2 балла)

    ✅Опишите в README.md корректные команды docker pull/run, которые должны привести к тому, что локально поднимется на inference ваша модель. Убедитесь, что вы можете протыкать его скриптом из пункта 3 (1 балл)

    ✅Проведите самооценку - распишите в реквесте какие пункты выполнили и на сколько баллов, укажите общую сумму баллов (1 балл)

Дополнительная часть:

    ✅Ваш сервис скачивает модель из S3 или любого другого хранилища при старте, путь для скачивания передается через переменные окружения (+2 доп балла)

    ✅Оптимизируйте размер docker image. Опишите в README.md, что вы предприняли для сокращения размера и каких результатов удалось добиться. Должно получиться мини исследование -- я сделал тото и получился такой-то результат (+2 доп балла) https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

    ✅Сделайте валидацию входных данных https://pydantic-docs.helpmanual.io/usage/validators/ . Например, порядок колонок не совпадает с трейном, типы, допустимые максимальные и минимальные значения. Проявите фантазию, это доп. баллы, проверка не должна быть тривиальной. Вы можете сохранить вместе с моделью доп информацию о структуре входных данных, если это нужно (+2 доп балла). https://fastapi.tiangolo.com/tutorial/handling-errors/ -- возращайте 400, в случае, если валидация не пройдена

Общая сумма баллов: 23


