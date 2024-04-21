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
This will start a local server, accessible at http://127.0.0.1:5000

### Test as an ADMIN user

To test the app as and admin user try logging in with credentials **username:** 'admin' and **password:** 'admin'.
If the schema.sql works as it should, you should be able to use the profile as an admin user now.

> In case the schema.sql failed to create an admin user, please refer to the admin_creation.txt for a readily made sql command
> to create a new admin profile with a hashed password. Credentials for this profile stay the same, username: admin and password: admin.