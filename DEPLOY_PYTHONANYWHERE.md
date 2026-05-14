# Публикация сайта на PythonAnywhere

## 1. Что загрузить

Загружайте на PythonAnywhere папку проекта `lapki_project`, но без:

- `.venv`
- `venv`
- `__pycache__`
- `staticfiles`
- `.env.local.ps1`
- `setup_local_mail.ps1`
- `run_local_server.ps1`
- `db.sqlite3` — только если хотите начать с пустой базы

Если хотите показать сайт уже с текущими питомцами, новостями и заявками, загрузите и `db.sqlite3`.

## 2. Создание web app

1. Зарегистрируйтесь на PythonAnywhere.
2. Откройте вкладку `Web`.
3. Нажмите `Add a new web app`.
4. Выберите `Manual configuration`.
5. Выберите `Python 3.10`.

## 3. Загрузка проекта

Самый простой путь:

1. Заархивируйте проект локально.
2. Загрузите архив через вкладку `Files`.
3. Распакуйте в домашнюю папку.

Итоговая структура должна быть примерно такой:

`/home/your_username/lapki_project/manage.py`

## 4. Виртуальное окружение и зависимости

Откройте `Bash console` и выполните:

```bash
cd ~/lapki_project
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5. Переменные окружения

В проекте уже есть безопасный шаблон:

[deploy.env.example](C:/Users/arina/Desktop/диплом/sait/lapki_project/deploy.env.example)

На вкладке `Web` в блоке `Environment variables` добавьте:

```text
DJANGO_SECRET_KEY=ваш_новый_секретный_ключ
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your_username.pythonanywhere.com,your_username.eu.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your_username.pythonanywhere.com,https://your_username.eu.pythonanywhere.com
```

Если хотите оставить отправку почты, добавьте ещё и почтовые переменные.
Но на бесплатном аккаунте SMTP может не работать.

## 6. Миграции и статика

В `Bash console`:

```bash
cd ~/lapki_project
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

Если нужно создать администратора:

```bash
python manage.py createsuperuser
```

## 7. Настройка virtualenv

На вкладке `Web` укажите:

`/home/your_username/lapki_project/.venv`

## 8. WSGI

Откройте `WSGI configuration file` и используйте такой блок:

```python
import os
import sys

path = '/home/your_username/lapki_project'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lapki_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 9. Static files

На вкладке `Web` добавьте:

- URL: `/static/`
- Directory: `/home/your_username/lapki_project/staticfiles`

Если нужно отдавать загруженные изображения:

- URL: `/media/`
- Directory: `/home/your_username/lapki_project/media`

## 10. Перезагрузка

Нажмите `Reload`.

После этого сайт должен открываться по ссылке:

`https://your_username.pythonanywhere.com`

## 11. Что проверить после публикации

- открывается главная страница
- открываются питомцы и новости
- работает подбор
- работает заявка на усыновление
- загружаются изображения
- открывается кабинет
- открывается админка

## 12. Важно

- для показа научному руководителю бесплатного PythonAnywhere обычно достаточно
- для реального приюта позже лучше перейти на PostgreSQL и более постоянный хостинг
- не храните реальные пароли почты в коде
