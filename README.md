# Instructions to execute API

1. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

2. Install external libraries

```
python3 -m pip install -r requirements.txt
```

3. Run app

```
python3 index.py
```

4. Ctrl + C to exit app

5. Use command 

```
deactivate
```

to exit from venv.

# Project structure
The architecture of project consider sections for tables definition (models), database connection, routes, scripts for automated processes, app configuration and general execution.

Execution of app uses index.py where port is established, and for new environment database is create.

To configure jwt, registration of routers for user and task directions and database location is verified in app.py file. Also, in case other database instead of sqlite is prefered, can be modified in .env file, in variable DATABASE_URI, taking advantage of SQLAlchemy ORM.

Object to manipulate the database is established in utils/db.py using ORM.

The definition of database tables is made from the models included in the models folder.

## User definition
- id PRIMARY KEY
- email STRING (max. extension 100)
- password STRING (max. extension 200)

## Task definition
- id PRIMARY KEY
- user_id INTEGER FOREING KEY pointing to id column from users table
- title STRING (max. extension 200)
- description STRING (max. extension 1000)
- completed BOOLEAN (by default, value is false)
- created_at DATETIME (by default considers actual datetime)

Scripts folder includes code for automated executions. In this case clean_tasks.py delete completed tasks. Instructions are added to to set up automation using cron.

# Documentation routes
API routes are divided into creation and logging users, and tasks manipulations

routes/users_route.py
Includes the routes
- POST /register
  Requires an email with correct format (email@service.com/, .org, .io, etc., are also valid) and password associated to that email.
  Fields are required as "email" and "password" in body request.
  Returns message and status explaining result of process.
- POST /login
  Requires previously registered email and its corresponding password. Creates a token for user, token is valid during 12 hours.
  Fields are required as "email" and "password" in body request.
  Returns message and status explaining result of process.

routes/tasks_route.py
- POST /tasks
  Requires title, description and token from previously logged in user.
  Fields to create task are required as "title" and "description".
  Returns message and status explaining result of process.
- GET /tasks
  Requires token from previously logged in user.
  Return message, status and list of tasks related to user.
- PATCH /tasks/<id>
  Change completed status for task with indicated id.
  It is verified if user owns taks so any user can not change outside tasks.
  Return message and status explaining result of process.


