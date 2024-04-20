# Проект «API для Yatube» (fork общего проекта)
Групповой проект по доработке программной части API для сервиса видеохостинга Yatube.

### При выполнении данного проекта были выполнены следующие задачи:

- Знакомство с работой в таск-трекере;
- Командная работа над проектом с помощью VCS git в общем репозитории на GitHub;
- Выполнение учатниками команды кросс-ревью;
- Выбор оптимального режима для совместной работы, учитывающего индивидульный график и сильные стороны каждого из участников команды;

### Авторы проекта:
- Гросс Евгения, тимлид, разработчик (разработка моделей отзывов, комментариев, рейтинга произведений) - https://github.com/EugeniaGross
- Журавлев Дмитрий, разработчик (разработка моделей произведений, категорий, жанров) - https://github.com/Forget-me-not-crossyroad
- Соколов Павел, разработчик (разработка системы регистрации, аутентификации, прав доступа, системы подтверждения через e-mail) - https://github.com/pavelVsokolov

### Технологии
[![Pytest Badge](https://img.shields.io/badge/-Python-blue?style=for-the-badge&labelColor=black&logo=python&logoColor=e535ab)](#)
[![Python Badge](https://img.shields.io/badge/-Python-blue?style=for-the-badge&labelColor=black&logo=python&logoColor=ffff00)](#)
[![VSCode Badge](https://img.shields.io/badge/-VSCode-blue?style=for-the-badge&labelColor=grey&logo=visualstudiocode&logoColor=white)](#)
[![Flake8 Badge](https://img.shields.io/badge/-Flake8-black?style=for-the-badge&labelColor=grey)](#)
[![Django Badge](https://img.shields.io/badge/-DRF-092E20?style=for-the-badge&labelColor=grey&logo=django&logoColor=white)](https://www.djangoproject.com/)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/EugeniaGross/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env или python3 -m pip install --upgrade pip
```

```
source venv/Scripts/activate (для Windows) или venv/bin/activate (для Linux)
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip или python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate или python3 manage.py migrate
```

Запустить проект:

```
python manage.py runserver или python3 manage.py runserver
```

Получить документацию API проекта при запущенном локально проекте:

```
http://127.0.0.1:8000/redoc/
```

Скачать и установить Postman для изучения API проекта:

```
https://www.postman.com/
```

Проверить работоспособность API проекта (GET-запрос):

```
GET http://127.0.0.1:8000/api/v1
```

