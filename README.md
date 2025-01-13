# ERH PROJECT GROUP()

## **Setup**

- create a virtual environment python `python -m  venv venv`
- activate virtual environment `venv\Scripts\activate`
- install requirements

```bash
pip install -r requirements.txt
```

- create database and add variables to .env file following the example.env

### **OR**

- if you have docker installed you can use the compose file to set it up
- optional: on localhost you can run the docker compose file to start up db

In .env file please place the following configuration

```bash
LIVE=development
DB_PORT=
MEDIA_PATH=assets
MAIL_SERVER=
MAIL_USERNAME=
MAIL_PASSWORD=
MYSQL_DATABASE_HOST=
SECRET_KEY=
DATABASE_URL=
```

- LIVE: development or production (development is to run in dev mode while production it to run in production mode)
- DB_PORT: database port eg: 5432
- MEDIA_PATH: path to store media files eg: assets (leave as assets for now)
- MAIL_SERVER: mail server or mail provider eg: smtp.goole.com
- MAIL_USERNAME: eg: os@gmail.com
- MAIL_PASSWORD: password for the mail eg: somevalue
- MYSQL_DATABASE_HOST: database host for mysql eg: localhost
- SECRETE_KEY: some random key eg:180eu04-4yyi@hjgkg
- DATABASE_URL: full db url eg: mysql+mysqlconnector://faithkoko:kpekuspass@localhost:9309/ehr_baby
