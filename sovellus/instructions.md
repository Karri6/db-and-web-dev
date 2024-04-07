# Instructions

### GIT clone
Start by cloning this repository or download the raw files to your computer.

### Create .env File
To begin with the user needs to create a new directory 'env_files' under the root directory (sovellus). Here the user needs to create two files:
- 'db_url.env', copy and paste the following line to the file:
```
DATABASE_URL=postgresql://pajar:paprikamajoneesi@localhost/webdev_db
```
- 'secret_key.env', copy and paste the following line to the file:
```
SECRET_KEY=h4g23e8fae6c3et5b724o8b4791aycd4
```

### Activate Virtual Environment
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

### Install Dependencies

```
  pip install -r requirements.txt
```

### Set Up Database Schema

```
  psql < schema.sql
```

### Run the Application
```
  flask run
```
> This command will start a local server, accessible at http://127.0.0.1:5000

