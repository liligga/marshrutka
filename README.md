# Как стартовать проект
Для того, чтоб установить зависимости, нужно выполнить команды
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
Для того чтобы запустить сервер, нужно выполнить команду
`uvicorn main:app --reload`
`uvicorn` - это сервер, `main` - это файл `main.py`, `app` - это инстанс приложения fastapi, и `--reload` - для того, чтобы сервер подгружал изменения в файлах, по умолчанию этого не происходит.


`main.py` - основной файл, с маршрутами
`database.py` - файл с предварительными данными
`models.py` - файл с моделями

# Работа с запросами
С GET запросами можно в принципе работать и в браузере, но наверное самый лучший и полезный инструмент, чтобы работать с любыми запросами - POSTMAN
При PUT запросе для изменения координат нужно формировать данные в body запроса в виде json:
`{"id": 2, "lat": 100,  "lng": 200}`, при этом для обрабатывания и валидации json данных используем pydantic