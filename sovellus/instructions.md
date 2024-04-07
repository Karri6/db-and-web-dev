# Instructions

## GIT clone
Start by cloning this repository or download the raw files to your computer.

## Create .env File
To begin, the user needs to create a new directory 'env_files' under the root directory (sovellus). Under this directory the user needs to create two files:
- First file is: 'db_url.env', copy and paste the following line to the file:
```
DATABASE_URL=postgresql://pajar:paprikamajoneesi@localhost/webdev_db
```
- The second file will be: 'secret_key.env', copy and paste the following line to the file:
```
SECRET_KEY=h4g23e8fae6c3et5b724o8b4791aycd4
```

## Activate Virtual Environment
**Unix-based systems:**

```
  python3 -m venv venv
  source venv/bin/activate
```

**For Windows:**

```
  python -m venv venv
  .\venv\Scripts\activate
```

## Install Dependencies
To make sure all necessary dependencies are in the virtual environment.
```
  pip install -r requirements.txt
```
> apologies in advance for possible currently extra dependencies, did not have time to remove redundant dependencies

## Set Up Database Schema
Configure the database schema using this command.
```
  psql < schema.sql
```

## Run the App
Use this command to launch the app.
```
  flask run
```
This will start a local server, accessible at http://127.0.0.1:5000

