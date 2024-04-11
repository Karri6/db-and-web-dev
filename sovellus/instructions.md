# Instructions
> Previous instructions had mistakenlu still my personal local psql address in the instructions, apologies for anyone that had to go through extra steps to get the program working.

## GIT clone
Start by cloning this repository or download the raw files to your computer.

## Set Up Database Schema
> These are the steps I took to ensure I got the database to work on another computer, if you have a better method feel free to use that.

Create new database with commands:
```
psql
user=# CREATE DATABASE <new_db_name>;
```
OR alternatively:
```
createdb -U <your_psql_user> <new_db_name>
```

Configure the database schema using this command.
```
psql -d <new_db_name> < schema.sql
```

If there are still issues


## Create .env Directory and Files
To begin, the user needs to create a new directory 'env_files' under the root directory (sovellus). Under this directory the user needs to create two files:
- First file is: 'db_url.env', copy and paste the following line to the file:
```
DATABASE_URL=postgresql://<new_db_name> 
```
> insert your local psql address here

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

## Run the App
Use this command to launch the app.
```
  flask run
```
This will start a local server, accessible at http://127.0.0.1:5000


