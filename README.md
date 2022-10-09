# Restaurant rating
Recruitment application. This is a system for rating restaurants in 3 categories: taste, size,  service

## How to configure the app

### Docker:

1. Create .env file with configuration:
   ```text
   DB_NAME=db_name
   DB_USER=db_user
   DB_PASSWORD=super_secret_password
   DB_HOST=db
   PGADMIN_EMAIL=pgadmin_email
   PGADMIN_PASSWORD=pgadmin_super_secret_password
   ```
2. When docker is installed, use command:
   ```commandline
   docker-compose up
   ```

### Locally:

1. It's a python based application, so you have to install python on your pc: [download python](https://www.python.org/downloads/)
2. Download the app or just clone it from repository
3. Create and enable virtual environment using command: `env\Scripts\activate.bat` [virtualenv PyPi](https://pypi.org/project/virtualenv/)
4. Install requirements.txt: `pip install -r requirements.txt`
5. Install database on your pc and configure it in db_config.py file. Default is SQLite, but Postgres is preferable.
   ``` 
    Note: If there won't be a .env file, python will use SQLite as default.
   ```
6. Create _env.py file to store the secrets locally. Required variables:
    ```
   DB_NAME=db_name
   DB_USER=db_user
   DB_PASSWORD=super_secret_password
   DB_HOST=db
   ```

7. Create database tables and fill restaurant table with rows using command:

        python management.py
8. Application can be used in two ways:
   ```
   As command line: python index.py --help
   As web aplication: Start app (python app_.py), use curl or postman for testing. 
   You can find endpoints in app_.py file. If you want rate restaurant, send post with request body as JSON. 
   Data required in schemas.py.
   ```