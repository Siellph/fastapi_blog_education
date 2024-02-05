9. Онлайн платформа для обучения с использованием Fast Api
    - Модели: Пользователи, Курсы, Уроки
    - Идея проекта: Разработка онлайн платформы для обучения с возможностью доступа к курсам (пусть будут просто файлы), просмотра уроков, выполнения заданий и авторизации пользователей.

Требования к проекту:
- Упаковка проекта в докер-компоуз и запуск через docker compose up без дополнительной настройки
- прохождение flake8 + mypy в соответствии с конфигурациями проекта
- Кеширование всего, что возможно закешировать через redis
- Orm:  sqlalchemy2.0
- Migration: alembic (необязательно т.к. не делали на парах)
- Тесты - pytest + mock на redis и rollback транзакций фикстур вместо удаления.
- Минимальные данные при разворачивании проекта (фикстуры)
- Метрики: 
  - На кол-во полученных запросов в разрезе каждой ручки.
  - На кол-во ошибок по каждой ручке
  - На кол-во отправленных запросов
  - Время выполнения каждой ручки в среднем (гистограмма)
  - Время выполнения всех интеграционных методов (запросы в бд, редис и тп (гистограмма))
- Валидация входящих данных (pydantic)
- Настройки в env
- Без дублирования кода
- poetry как сборщик пакетов
- Обработка ошибок и соответствующие статусы ответов
- В README.md ожидается увидеть как что работает, чтобы можно было ознакомиться проще с проектом
___
**Логика работы**

* Пользователи имеют возможность просматривать доступные курсы, записываться на них и отслеживать свой прогресс.
* Преподаватели могут создавать и редактировать курсы и уроки, назначать задания и проверять их выполнение.
* Предусмотрена возможность загрузки и хранения учебных материалов, включая текстовые файлы, изображения и видео.
___
**Стэк технологий**
___
+ :rocket: Framework: FAST API
+ ORM: SQLAlchemy2.0
+ Pydantic
+ :scroll: Poetry
+ :ship: Docker
+ :snake: Python 3.11
___
Перед запуском проекта необходимо создать:
1. Файл `.env` в папке `/grafana`. Пример находится в файле '/grafana/env.example'
2. Файл `.env` в папке `/conf`. Пример находится в файле '/conf/env.example'
___
Для запуска проекта на локальном ПК используется следующая команда
```
sudo docker-compose up
```
___
При запуске проекта разворачиваются контейнеры и соответствующие им образы со следующими именами:

|Имя контейнера        |Описание|
|----------------------|--------|
|prometheus            |Система мониторинга предназначенная для сбора и анализа метрических данных о работе приложений и инфраструктуры|
|grafana               |Открытое ПО для визуализации данных и мониторинга. Предоставляет гибкие инструменты для создания интерактивных и информативных дашбордов|
|web                   |Контейнер с основным проектом|
|fastapi_blog-console-1|Консоль приложения|
|web_db                |Контейнер с БД|
|fastapi_blog-minio-1  |Объектное хранилище данных с открытым исходным кодом, разработанное для обеспечения хранения и управления большими объемами данных в виде объектов|
|redis                 |Высокопроизводительная система управления базами данных, использующая в памяти хранение данных и работающая по принципу ключ-значение|
___
*Для просмотра контейнеров:*
```
sudo docker container ls
```

*Для просмотра образов:*
```
sudo docker image ls
```
*Для того чтобы просмотреть имеющиеся volume:*
```
sudo docker volume ls
```
*Для того чтобы очистить БД необходимо удалить volume:*
```
sudo docker volume rm [volume_name]
```
___
Для быстрого удаления всех контейнеров, образов и данных из Docker можно воспользоваться следующим набором комманд
```
sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images -f "dangling=true" -q)
sudo docker rmi $(sudo docker images -a -q)
sudo docker volume prune
sudo docker volume rm fastapi_blog_prom_data
sudo docker system prune -a
```
___
**После запуска проекта доступны:**

|Название     |URL  |
|-------------|-----|
|Документация | http://0.0.0.0:8000/swagger|
|Метрика      | http://0.0.0.0:8000/metrics|
|Prometheus   | http://0.0.0.0:9090|
|Grafana      | http://0.0.0.0:3000/login|
|MinIO        | http://0.0.0.0:9001/login|

___
🏎️ **Roadmap**

- [X] Модели SQLAlchemy
- [X] Фикстуры
- [X] Миграции
- [X] Схемы Pydantic
- [X] CRUD
- [X] Эндпоинты
- [X] Обработка исключений
- [X] Метрики
- [X] Кэширование данных
- [X] Тесты

**Эндпоинты**

***

**Пользователи:**

<details>

<summary>Регистрация пользователя</summary>

`[POST] /users/signup`
- Регистрация новых пользователей на платформе, включая получение данных пользователя, таких как имя, электронная почта и пароль.

</details>

<details>

<summary>Аутентификация пользователя</summary>

`[POST] /auth/login`
- Аутентификация пользователей для доступа к защищенным ресурсам, включает в себя проверку электронной почты и пароля.

</details>

<details>

<summary>Получение информации о пользователе</summary>

`[GET] /users/me`
- Позволяет аутентифицированным пользователям получать информацию о своем профиле.

</details>

***

**Курсы:**


<details>

<summary>Создание курса</summary>

`[POST] /courses`
- Позволяет преподавателям или администраторам создавать новые курсы, указывая название, описание, категорию и другую информацию о курсе.

</details>

<details>

<summary>Просмотр списка курсов</summary>

`[GET] /courses`
- Возвращает список всех доступных курсов, возможно с фильтрацией по категориям, уровню сложности и т.д.

</details>

<details>

<summary>Получение детальной информации о курсе</summary>

`[GET] /courses/{course_id}`
- Возвращает детальную информацию о конкретном курсе, включая список уроков, материалы и задания.

</details>

<details>

<summary>Обновление информации о курсе</summary>

`[PUT] /courses/{course_id}`
- Позволяет преподавателям или администраторам обновлять информацию о курсе.

</details>

<details>

<summary>Удаление курса</summary>

`[DELETE] /courses/{course_id}`
- Удаляет курс, доступно только для преподавателей или администраторов.

</details>

***

**Уроки:**

<details>

<summary>Добавление урока в курс</summary>

`[POST] /courses/{course_id}/lessons`
- Позволяет добавлять новые уроки в курс, требует указания названия урока, содержания и прочих материалов.

</details>

<details>

<summary>Просмотр списка уроков курса</summary>

`[GET] /courses/{course_id}/lessons`
- Возвращает список уроков, относящихся к конкретному курсу.

</details>

<details>

<summary>Получение информации об уроке</summary>

`[GET]
- *URL:* `/courses/{course_id}/lessons/{lesson_id}`
- Возвращает детальную информацию об уроке, включая содержание и доступные материалы.

</details>

<details>

<summary>Обновление урока</summary>

`[PUT] /courses/{course_id}/lessons/{lesson_id}`
- Позволяет преподавателям обновлять информацию об уроке, включая название, содержание и материалы.

</details>

<details>

<summary>Удаление урока из курса</summary>

`[DELETE] /courses/{course_id}/lessons/{lesson_id}`
- Удаляет урок из курса, доступно только для преподавателей или администраторов.

</details>

***

**Работа с файлами:**

<details>

<summary>Загрузка файла для урока</summary>

`[POST] /courses/{course_id}/lessons/{lesson_id}/upload`
- Этот эндпоинт позволяет преподавателям загружать файлы, связанные с уроком. Можно использовать для загрузки учебных материалов, заданий или дополнительных ресурсов.
- *Тело запроса:* `FormData` с файлом.

</details>

<details>

<summary>Получение списка файлов урока</summary>

`[GET] /courses/{course_id}/lessons/{lesson_id}/files`
- Возвращает список файлов, загруженных для конкретного урока, позволяя студентам просматривать и скачивать доступные материалы.

</details>

<details>

<summary>Скачивание файла урока</summary>

`[GET] /courses/{course_id}/lessons/{lesson_id}/files/{file_id}`
- Позволяет скачать конкретный файл, связанный с уроком. Этот эндпоинт обеспечивает доступ к учебным материалам, видео, документам и другим файлам.

</details>

<details>

<summary>Удаление файла урока</summary>

`[DELETE] /courses/{course_id}/lessons/{lesson_id}/files/{file_id}`
- Позволяет преподавателям удалять ранее загруженные файлы из урока, что может быть полезно при обновлении или исправлении учебных материалов.

</details>