## Тестовое задание на вакансию Junior Python Backend Developer (АпТрейдер)

#### Выполнила Нина Сперанская
#### Контакты:
тел. +7 (705) 786-75-06 (Казахстан)  
email: nina.speranskaya35@gmail.com  
Telegram: [@Hunteena](https://t.me/Hunteena)  
портфолио: [https://github.com/Hunteena](https://github.com/Hunteena)

### Задача: 
отрисовка древовидного меню с помощью templatetag, сделав только один запрос к базе данных.
### Локальный запуск проекта


1. Клонировать репозиторий на свой компьютер  
    ```
    git clone https://github.com/Hunteena/UpTrader/
    ```
1. Создать файл `.env` с переменными окружения, аналогичный [.env.template](.env.template)
1. Создать и провести миграции  
    ```
    python manage.py makemigrations menutree
    python manage.py migrate
    ```
1. Загрузить пример базы данных (по желанию)  
    ```
    python manage.py loaddata example.json
    ```
1. Создать суперпользователя для входа в административную панель  
    ```
    python manage.py createsuperuser
    ```
1. Запустить сервер  
    ```
    python manage.py runserver
    ```

После успешного запуска сервера доступны следующие адреса:

- [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) - административная панель Django, 
- [Древовидное меню](http://127.0.0.1:8000/) - пример работы приложения по отрисовке меню 
(если был загружен пример базы данных; иначе необходимо внести данные через административную панель).
