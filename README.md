## Petstore API autotest

**Сценарий:**
1) POST /user/createWithList
2) GET /user/{username}
3) Валидация полей ответа

**Используемые технологии:**
- Python 3.10+
- pytest
- requests
- allure-pytest

**Установка зависимостей**
- pip install -r requirements.txt

**Запуск тестов**
- pytest -m api

**Просмотр Allure отчета**
- allure serve allure-results
