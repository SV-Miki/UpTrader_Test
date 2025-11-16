# Up Trader Test

Выполненное тестовое задание

## Функции

- Меню хранится в базе данных (`Menu` и `MenuItem`).
- Поддержка вложенных пунктов меню.
- Активный пункт меню определяется по текущему URL.
- Раскрыты все уровни над активным пунктом и первый уровень вложенности под ним.
- Меню редактируется через стандартную админку Django.
- Можно выводить несколько меню на одной странице по имени.
- Переход по URL реализован через явный URL или named URL.
- Для построения дерева меню используется только 1 запрос к таблице `MenuItem`.

## Структура проекта

```
UpTrader/
├─ config/
│  ├─ init.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ menus/
│  ├─ init.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ views.py
│  ├─ migrations/
│  ├─ static/
│  │  └─ menus/
│  │     └─ menu.css     # CSS для отображения активного пункта
│  ├─ templates/
│  │  └─ menus/
│  │     ├─ menu.html
│  │     └─ menu_item.html
│  └─ templatetags/
│     ├─ init.py
│     └─ menu_tags.py
├─ templates/
│  └─ base.html
├─ venv/
├─ .gitignore
├─ db.sqlite3
├─ manage.py
└─ README.md
```

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone <your-repo-url>
cd UpTrader
```

2. Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3.	Установите зависимости:

```commandline
pip install django
```

4.	Примените миграции:
```commandline
python manage.py migrate
```

5.	Создайте суперпользователя для доступа к админке:
```commandline
python manage.py createsuperuser
```

6.	Запустите сервер:
```commandline
python manage.py runserver
```

7.	Перейдите на ```http://127.0.0.1:8000/admin```, создайте меню и пункты меню.
Вставляйте меню в шаблон с помощью template tag:

```
{% load static menu_tags %}
<link rel="stylesheet" href="{% static 'menus/menu.css' %}">

{% draw_menu 'main_menu' %}
```

Шаблоны и стили
* menus/menu.html — контейнер меню.
* menus/menu_item.html — рекурсивный пункт меню.
* menus/static/menus/menu.css — базовые стили меню.
* templates/base.html — пример использования меню на странице.

Примечания
* Меню строится с помощью template tag draw_menu.
* Активные пункты подсвечиваются, вложенные элементы автоматически раскрываются.
* Поддерживаются как явные URL, так и named URL.

---