# chessphere
## Chess Tournament management system (simulation) written in Django and Django REST framework. 

## Table of Contents
- [Installation](#installation)
- [Database Design](#database-design)

## Installation
1. Clone the repo:
    ```sh
    git clone https://github.com/Samandar-Komilov/chessphere.git
    ```
2. Navigate to the project directory:
    ```sh
    cd chessphere
    ```
3. Initiate a virtual environment (pipenv):
    ```sh
    pipenv shell
    ```
3. Install dependencies:
    ```sh
    pipenv install -r requirements.txt
    ```
4. Create .env file and specify your postgres database credentials:
    ```.env
    DB_NAME = <your_db_name>
    DB_USER = <your_db_user>
    DB_PASSWORD = <your_db_password>
    DB_HOST = <your_db_host>
    ```
5. Migrate database:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Run the project:
    ```sh
    python manage.py runserver
    ```

## Database Design

![ER Diagram](chessphere_dbschema.png)
