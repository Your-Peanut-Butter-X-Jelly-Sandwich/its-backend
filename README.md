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

## Set up third party login

- Naviage to `http://127.0.0.1:8000/admin`
- Modify the entry in `Sites` table to be
  - Domain name: `http://127.0.0.1:8000/`
  - Display name: `http://127.0.0.1:8000/`

### Google

- Navigate to Google Cloud Console
- Create new project
- Authorized redirect URIs = `http://127.0.0.1:8000/auth/google/login/callback/`
- Authorized JavaScript origins = `http://127.0.0.1:8000` and `http://localhost:3000`
- Naviage to `http://127.0.0.1:8000/admin`
- Use the client ID and client secret generated to create a database entry in the `Social application` table with `Provider`: Google
- Select `http://127.0.0.1:8000/` into the `Chosen sites`

### Github

- Navigate to `https://github.com/settings/applications/new`
- Application Name: `Intellient Tutoring System`
- Homepage URL: `http://localhost:8000/`
- Authorization callback URL: `http://localhost:8000/auth/social/callback`
- Use the client ID and client secret generated to create another entry in the `Social application` table with `Provider`: Github
- Select `http://127.0.0.1:8000/` into the `Chosen sites`

## Start Application

- Start server by running `python manage.py runserver`
