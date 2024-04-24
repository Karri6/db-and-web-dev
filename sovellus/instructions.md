# Instructions
> Previous instructions had mistakenly still my personal local psql address in the instructions, apologies for anyone that had to go through extra steps to get the program working.

## GIT clone
Start by cloning this repository or download the raw files to your computer.

- **Note that the root directory for the project is 'db-and-web-dev/sovellus/' which means, while setting up the app, all files should go under the 'sovellus/' directory. Leaving files to the upper 'db-and-web-dev/' directory may cause the app to not function as intended**

## Set Up Database Schema
> These are the steps I took to get the database copied and running on another computer, if you have a better method feel free to use that. 

Create new database with commands:
```
psql
user=# CREATE DATABASE <new_db_name>;
```
OR alternatively:
```
createdb -U <your_psql_username> <new_db_name>
```

Configure the database schema using this command.
```
psql -d <new_db_name> < schema.sql
```

After succesfully configuring the database, use this command to create an admin role user manually.
```
INSERT INTO users (username, password, role) VALUES
('admin', 'scrypt:32768:8:1$4qWkuzowHTmuql0z$487a07924cda4545a5c38fed3f2381fd06c5a87e9d147828abd83db59525eba91da3555c4e4734912f1e2db6a3fa9efc793a295a37a6cf009eeb3c74b3ce10de', 'admin');
```
- This is a readily made sql command to create a new **admin** profile with a hashed password. Credentials for this profile are username: admin and password: admin.
> The admin_creation.txt has the same sql command that you can copy and paste to the cmd while configuring the db.

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
> You can also generate your own secret key if you want to.

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
This will start a local server, accessible at 'http://127.0.0.1:5000'

### Test as an ADMIN user

To test the app as and admin user try logging in with credentials **username:** 'admin' and **password:** 'admin'.
If you have completed the steps to configure the database, you should be able to use the application as an admin user now.

