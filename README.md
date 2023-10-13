## Запуск проекта

```
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
- Для запуска на машине должен быть установвлен python не ниже версии 3.10.
- Строка подключения к mongodb берется из переменной окружения `MONGO_URI`. Значение по умолчанию хранится в файле [`.env`](.env).

## Запуск проекта в docker

```
docker compose up --build -d
```