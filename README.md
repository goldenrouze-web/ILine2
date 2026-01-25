Employee CRM (Flask + SQLAlchemy)
Простой веб-каталог сотрудников с возможностью поиска, сортировки и изменения начальника.

Требования
Python 3.7+
Flask 2+
SQLAlchemy 1.4+
PyMySQL (для MySQL) или psycopg2-binary (для PostgreSQL)

Структура проекта
employee_crm/
├── app.py
├── models.py
├── requirements.txt
├── README.md
├── templates/
│   ├── employees.html
│   └── add_employee.html
└── venv/

Установка.

1. Клонирование репозитория

git clone <URL_REPO>
cd employee_crm

2. Создание виртуального окружения
Mac / Linux:

python3 -m venv venv
source venv/bin/activate

Windows (PowerShell):

python -m venv venv
.\venv\Scripts\Activate.ps1

(После активации окружения должно появиться (venv) в терминале)

3. Установка зависимостей

pip install --upgrade pip
pip install -r requirements.txt

4. Настройка базы данных:

MySQL

Создайте базу данных:

CREATE DATABASE employees_db;
CREATE USER 'crmuser'@'localhost' IDENTIFIED BY 'crm123';
GRANT ALL PRIVILEGES ON employees_db.* TO 'crmuser'@'localhost';
FLUSH PRIVILEGES;

Настройка переменной окружения:
export DATABASE_URL="mysql+pymysql://crmuser:crm123@localhost:3306/employees_db"
export SECRET_KEY="your_secret_key"

PostgreSQL

Создайте базу и пользователя:

CREATE DATABASE employees_db;
CREATE USER crmuser WITH PASSWORD 'crm123';
GRANT ALL PRIVILEGES ON DATABASE employees_db TO crmuser;

Переменная окружения:

export DATABASE_URL="postgresql+psycopg2://crmuser:crm123@localhost:5432/employees_db"
export SECRET_KEY="your_secret_key"

(для Windows используйте set вместо export)

5. Создание таблиц

Таблицы создаются автоматически при первом запуске app.py благодаря:
Base.metadata.create_all(engine)

6. Запуск приложения

python app.py
(пПо умолчанию Flask запустится на http://127.0.0.1:5000/employees)



Использование.

Просмотр сотрудников: /employees
Поиск по ФИО: ввод текста в поле поиска
Сортировка: кликаем по заголовкам таблицы (ID, ФИО, должность, дата, зарплата)
Добавление сотрудника: /add_employee
Изменение начальника: в таблице сотрудников вводим ID нового начальника