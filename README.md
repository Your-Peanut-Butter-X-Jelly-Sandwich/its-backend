# Quick Start

## Creating a virtual environment to isolate our package dependencies locally

It is suggested to have a dedicated virtual environment for each Django project, and one way to manage a virtual environment is venv, which is included in Python.

- `cd` into `its_backend` directory, run the following command to install Python 3.11

  - ```bash
    pyenv install 3.11.4
    ```

  - If you do not have `pyenv` , follow the guide [here](https://github.com/pyenv/pyenv#installation) to install it on your machine and set up your shell environment

- Create a virtual environment to isolate our package dependencies locally.

  - ```bash
    ${pyenv root}/versions/3.11.4/bin/python -m venv --upgrade-deps --copies its_env
    ```

## Install dependencies

- `cd` into `its_backend`
- activate the virtual environment by running

  - ```bash
    source its_env/bin/activate # On Windows use env\Scripts\activate
    ```

- install dependencies by running

  - ```bash
    pip install -r ../requirement.txt
    ```

## Database Migration

- Create migrations by running `python manage.py makemigrations`
- Sometimes Django might now detect the changes in individual apps, in that case, do `python manage.py makemigrations --empty [APP_NAME]
- Run migrations  `python manage.py migrate`
- You might encounter this issue: `django.db.migrations.exceptions.InconsistentMigrationHistory: Migration accounts.0001_initial is applied before its dependency auth.0012_alter_user_first_name_max_length on database 'default'.`
  - refer to this [post](https://stackoverflow.com/questions/65562875/migration-admin-0001-initial-is-applied-before-its-dependency-app-0001-initial-o) for solution

## Set up third party login

- Naviage to `http://127.0.0.1:8000/admin`
- Modify the entry in `Sites` table to be
  - Domain name: `http://127.0.0.1:8000/`
  - Display name: `http://127.0.0.1:8000/`

### Google

- Navigate to [Google Cloud Console](https://console.cloud.google.com)
- Create new project
- Authorized redirect URIs = `http://127.0.0.1:8000/auth/google/login/callback/`
- Authorized JavaScript origins = `http://127.0.0.1:8000` and `http://localhost:3000`
- Naviage to `http://127.0.0.1:8000/admin`
- Use the `client ID` and `client secret` generated to create a database entry in the `Social application` table with `Provider`: Google
- Select `http://127.0.0.1:8000/` into the `Chosen sites`
- To see a list of all OAuth Apps created: open the console left side menu and select APIs & services -> `Credentials`

### Github

- Navigate to `https://github.com/settings/applications/new`
- Application Name: `Intellient Tutoring System`
- Homepage URL: `http://localhost:8000/`
- Authorization callback URL: `http://localhost:8000/auth/social/callback`
- Use the client ID and client secret generated to create another entry in the `Social application` table with `Provider`: Github
- Select `http://127.0.0.1:8000/` into the `Chosen sites`
- To see a list of all OAuth Apps created: `settings` -> `<> Developer settings` -> `OAuth Apps`

## Start Application

- Start server by running `python manage.py runserver`

## View all urls created

run `python manage.py show_urls`

## Debug

- set `DEBUG=TRUE` in `settings.py`

- The typical usage to break into the debugger is to insert
  - `import pdb; pdb.set_trace()` or
  - `breakpoint()`
