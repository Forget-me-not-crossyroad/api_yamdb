# Проект «API для Yatube»
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
<img src="https://camo.githubusercontent.com/fb8731f93b7bc9ac1d530eac09d2e739be7248fd119a7a8e81d11514eafe5a49/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d5079746573742d6535333561623f7374796c653d666f722d7468652d6261646765266c6162656c436f6c6f723d626c61636b266c6f676f3d507974657374266c6f676f436f6c6f723d653533356162" alt="Pytest Badge" data-canonical-src="https://img.shields.io/badge/-Pytest-e535ab?style=for-the-badge&amp;labelColor=black&amp;logo=Pytest&amp;logoColor=e535ab" style="max-width: 100%;"> <img src="https://camo.githubusercontent.com/6f821a8c6c5575e343061f1d2720d6c13db74798bc715d7f6f9f26ab9b361c7e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d507974686f6e2d6666666630303f7374796c653d666f722d7468652d6261646765266c6162656c436f6c6f723d626c61636b266c6f676f3d507974686f6e266c6f676f436f6c6f723d666666663030" alt="Python Badge" data-canonical-src="https://img.shields.io/badge/-Python-ffff00?style=for-the-badge&amp;labelColor=black&amp;logo=Python&amp;logoColor=ffff00" style="max-width: 100%;"> [![VSCode Badge](https://img.shields.io/badge/-VSCode-blue?style=for-the-badge&labelColor=grey&logo=visualstudiocode&logoColor=white)](#) [![Flake8 Badge](https://img.shields.io/badge/-Flake8-black?style=for-the-badge&labelColor=grey)](#) [![Django Badge](https://img.shields.io/badge/-DRF-092E20?style=for-the-badge&labelColor=grey&logo=django&logoColor=white)](https://www.djangoproject.com/)

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

