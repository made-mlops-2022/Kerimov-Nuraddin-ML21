ml_project
==============================

HW1 for MLops By Kerimov  Nuraddin

Модели: catboost, logistic regression

Обучение:

на конфиге для catboost:
~~~
python -m ml_example.train --config-name=train_config_catboost
~~~

на конфиге для Logreg:
~~~
python -m ml_example.train --config-name=train_config_linear
~~~


Prediction
~~~
python -m ml_example.predict путь_к_данным путь_к_модели путь_предсказаний
~~~

Создание фейковых данных
~~~
python -m ml_example.data.make_dataset путь_выхода количество_объектов

python -m ml_example.data.make_dataset fake_data.csv 1000
~~~

✅В описании к пулл реквесту описаны основные "архитектурные" и тактические решения, которые сделаны в вашей работе. В общем, описание того, что именно вы сделали и для чего, чтобы вашим ревьюерам было легче понять ваш код (1 балл) 

✅В пулл-реквесте проведена самооценка, распишите по каждому пункту выполнен ли критерий или нет и на сколько баллов(частично или полностью) (1 балл) 

✅Выполнено EDA, закоммитьте ноутбук в папку с ноутбуками (1 балл) Вы так же можете построить в ноутбуке прототип(если это вписывается в ваш стиль работы) (только ноутбук) (1 балл)

⛔Использовать не ноутбук, а скрипт, который сгенерит отчет, закоммитьте и скрипт и отчет 

✅Написана функция/класс для тренировки модели, вызов оформлен как утилита командной строки, записана в readme инструкцию по запуску (3 балла) 

✅Написана функция/класс predict (вызов оформлен как утилита командной строки), которая примет на вход артефакт/ы от обучения, тестовую выборку (без меток) и запишет предикт по заданному пути, инструкция по вызову записана в readme (3 балла)

✅Проект имеет модульную структуру (2 балла)

✅Использованы логгеры (2 балла)

✅Написаны тесты на отдельные модули и на прогон обучения и predict (3 балла)

✅Для тестов генерируются синтетические данные, приближенные к реальным (2 балла)


✅Обучение модели конфигурируется с помощью конфигов в json или yaml, закоммитьте как минимум 2 корректные конфигурации, с помощью которых можно обучить модель (разные модели, стратегии split, preprocessing) (3 балла) (у меня catboost и logreg)

✅Используются датаклассы для сущностей из конфига, а не голые dict (2 балла)

✅Напишите кастомный трансформер и протестируйте его (3 балла) https://towardsdatascience.com/pipelines-custom-transformers-in-scikit-learn-the-step-by-step-guide-with-python-code-4a7d9b068156

✅В проекте зафиксированы все зависимости (1 балл)

✅Настроен CI для прогона тестов, линтера на основе github actions (3 балла). Пример с пары: https://github.com/demo-ml-cicd/ml-python-package
Дополнительные баллы=)

✅Используйте hydra для конфигурирования (https://hydra.cc/docs/intro/) - 3 балла

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
