## Используемые технологии
- python в качестве основного языка программирования
- javascript для скриптов в mongodb
- fastapi для rest-api приложения
- mongodb как основное хранилище данных
- elasticsearch для полнотекстового поиска
- memcached в качестве кэширования
- docker для виртуализации
- docker-compose для оркестрации и запуска кластера
- nginx в качестве балансировщика нагрузки

## Сценарии использования:
- Сохранение информации о студенте
- Получение информации о студенте по его id
- Получение списка всех студентов
- Получение списка студентов по имени
- Удаление информации о студенте

## Конфигурация приложения
Переменные окружения по умолчанию хранятся в файле [`.env`](.env).

| Переменная| Назначение                        |
| -------- |-----------------------------------|
|MONGO_URI| Строка подключения к mongodb      |
|ELASTICSEARCH_URI| Адрес elasticsearch               |
|MEMCACHED_URI| Адрес memcached                   |
|MONGO_DB| Используемая база данных mongodb  |
|MONGO_COLLECTION| Используемая коллекция mongodb    |
|ELASTICSEARCH_INDEX| Используемый индекс elasticsearch |

## Запуск проекта локально
Системные требования:
- Экземпляр mongodb, запущенный на localhost:27017
- Экземпляр elasticseacrh, запущенный на localhost:9200
- Экземпляр memcached, запущенный на localhost:11211

Запуск:
```
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Запуск кластера в docker
Системные требования:
- Запущенный демон docker на машине
- Желательно большое количество оперативной памяти(>16gb)

Запуск:
```
docker compose up --build -d
```


Trobleshooting:

В случае возникновения в elasticsearch ошибки
```
ERROR: [1] bootstrap checks failed
[1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```
Необходимо в wsl выставить переменную vm.max_map_count в необходимое значение:
```
wsl -d docker-desktop
sysctl -w vm.max_map_count=262144
```