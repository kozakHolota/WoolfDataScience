Ось пропонований вміст файлу README.MD для папки home_works/system_fundamentals/final_project. Скопіюйте його в новий файл у зазначеній директорії.

# Final Project: HTTP сервер + Socket сервер + MongoDB

Цей проєкт складається з двох Python-сервісів та MongoDB:
- HTTP сервер — обробляє HTTP-запити й віддає HTML/UI.
- Socket сервер — обробляє бізнес-логіку, працює із MongoDB.
- MongoDB — зберігає повідомлення та інші дані.

Запуск і оркестрація сервісів виконуються через docker-compose.

## Структура проєкту

- docker-compose.yaml — описує мультиконтейнерне середовище.
- mongo_data/ — том для збереження даних MongoDB (мапиться в контейнер /data/db).
- http_server/
  - Dockerfile — збірка образу HTTP сервера.
  - server.py — вхідна точка HTTP сервера.
  - endpoints.py, http_parts.py, non_routed_pages.py, util.py — логіка роутів та утиліти.
  - config.yaml — конфігурація HTTP сервера.
  - requirements.txt — Python-залежності для HTTP сервера.
  - html/ — шаблони та частини сторінок (template.html, index_part.html, login_part.html, message_part.html, search_results_part.html, error_part.html, style.css).
  - img/ — статичні зображення (якщо використовуються).
- socket_server/
  - Dockerfile — збірка образу Socket сервера.
  - server.py — вхідна точка Socket сервера.
  - endpoints.py, util.py — логіка обробки подій і допоміжні функції.
  - config.yaml — конфігурація Socket сервера.
  - requirements.txt — Python-залежності для Socket сервера.

Порти:
- HTTP сервер: 3000 (localhost:3000)
- Socket сервер: 5001 (localhost:5001)
- MongoDB: 27017 (localhost:27017)

За замовчуванням Socket сервер використовує підключення до Mongo через змінну середовища:
- MONGO_URL=mongodb://mongo:27017/dummy_messages

## Вимоги

- Docker і Docker Compose встановлені локально
- Вільні порти 3000, 5001, 27017 (або змініть мапінг у docker-compose.yaml)

## Швидкий старт через Docker Compose

1) Зібрати образи та запустити всі сервіси у фоновому режимі:
```shell script
bash
docker compose up -d --build
```


2) Перевірити статус контейнерів:
```shell script
bash
docker compose ps
```


3) Відкрити застосунок у браузері:
- Головна сторінка: http://localhost:3000/

Зупинити середовище:
```shell script
bash
docker compose down
```


Зберегти дані Mongo між запусками:
- Дані зберігаються в локальній теці mongo_data/ завдяки volume-мапінгу.

## Локальна збірка образів (за бажанням)

Якщо потрібно вручну зібрати окремі образи:

- HTTP сервер:
```shell script
bash
docker build -t final_project-http ./home_works/system_fundamentals/final_project/http_server
```


- Socket сервер:
```shell script
bash
docker build -t final_project-socket ./home_works/system_fundamentals/final_project/socket_server
```


Рекомендується все ж використовувати docker-compose для спрощення мережі, залежностей і healthcheck’ів.

## Налаштування середовища

- Змінна середовища для Socket сервера:
  - MONGO_URL — налаштована у docker-compose.yaml (mongodb://mongo:27017/dummy_messages)
- HTTP сервер очікує доступність Socket сервера (compose вирішує залежність через depends_on).

## Як це працює

- HTTP сервер віддає HTML-сторінки та взаємодіє із Socket сервером.
- Socket сервер зберігає та читає дані з MongoDB (БД dummy_messages).
- У директорії http_server/html ви знайдете основний шаблон та частини сторінок:
  - template.html — базовий шаблон
  - index_part.html — головна сторінка
  - login_part.html — сторінка входу
  - message_part.html — перегляд/відправка повідомлень
  - search_results_part.html — сторінка результатів пошуку
  - error_part.html — відображення помилок
  - style.css — стилі

Конкретні HTTP-роути та логіка описані у файлах http_server/endpoints.py і пов’язаних модулях.

## Перевірка підключення до БД

Після старту контейнерів:
```shell script
bash
docker exec -it mongo mongosh --quiet
```

У консолі Mongo:
```shell script
bash
use dummy_messages
db.runCommand({ ping: 1 })
```


## Вирішення типових проблем

- Порт зайнятий: змініть мапінги портів у docker-compose.yaml.
- Mongo не встигає піднятися:
  - У складі compose налаштовано healthcheck для Mongo та залежність socket_server від здорового стану Mongo.
  - Дочекайтесь, поки healthcheck стане healthy:
```shell script
bash
docker compose ps
```

- Оновлення залежностей:
  - Оскільки використовується Docker, після змін у requirements.txt перезберіть образи:
```shell script
bash
docker compose build
docker compose up -d
```


## Корисні команди

Логи:
```shell script
bash
docker compose logs -f http_server
docker compose logs -f socket_server
docker compose logs -f mongo
```


Перезапуск одного сервісу:
```shell script
bash
docker compose restart http_server
```


Знищити контейнери, мережі та залишити дані БД:
```shell script
bash
docker compose down
```


Повністю очистити, включно з даними:
```shell script
bash
docker compose down -v
```


Якщо потрібні правки або розширення README.MD — скажіть, я, AI Assistant, оновлю.