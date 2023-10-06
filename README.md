## Запуск проекта

```
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Строка подключения к mongodb берется из переменной окружения `MONGO_URI`. Значение по умолчанию хранится в файле [`.env`](.env).

## Запуск проекта в docker

```
docker compose up --build -d
```