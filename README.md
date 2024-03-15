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

## Test APIs

Our project uses Postman collections and [`newman`](https://www.npmjs.com/package/newman) to test our Django APIs.

### Run tests

Check that you have the `newman` package installed in your shell environment by running

```shell
$ newman --version
6.1.1
```

If your shell cannot find the `newman` package, download it using NPM or Homebrew:

```shell
$ npm install [-g] newman
$ brew install newman
```

Alternatively, you can `cd` into `test` folder and install dependencies:

```shell
$ cd test
$ npm install
```

After the package is downloaded, run your Postman collection by running:

```shell
$ chmod +x ./test/test.sh  # if necessary
$ ./test/test.sh  # or ./test.sh if you cd-ed into test
```

A sample [test Postman collection](./test/ITS-API-Test.postman_collection.json) is already included under the `test` folder. If you want to test your own collection, add your collection under the `test` folder and update the `POSTMAN_COLLECTION` value inside the [test script](./test/test.sh).

### Add test cases

To add test cases to the existing Postman collection, download the json file and import it to your local (or web) Postman application.

You will see that our Postman collection is structured hierarchically, with each collection and subcollection organized according to its respective tests. Here is an overview of how our tests are organized:

```
[01] Test collection 1
|--- [01] test request 1 - success
|--- [02] test request 2 - fail (reason for failure)
|--- ...
[02] Test collection 2
|--- [01] Test subcollection 1
     |--- [01] Test request 1 - status
     |--- [02] Test request 2 - status
     |--- ...
|--- [02] Test subcollection 2
     |--- ...
...
```

The `[xx]` numbering scheme in the names do not really matter as Postman does not inherently sort the collections by name, but it helps give a clear picture on the order of the tests. To add your own test cases, simply add a folder to the end and add test requests under your folder. Try to follow the naming scheme of our test collection.

See Postman's [documentation](https://learning.postman.com/docs/writing-scripts/test-scripts/) on the basics of writing test scripts in Postman.

To test endpoints that require authorization (student, tutor, or manager), you can use the bearer tokens that are configured in the first test collection (`[01] Get access tokens`).

```
{{tutor_bearer}}
{{student_bearer}}
```

Add one of the above in your request's `Authorization` tab with type `Bearer token`.

## Ruff Linter

Our project uses [`ruff`](https://docs.astral.sh/ruff/) to lint our code and maintain a clean codebase.

### Lint Rules used in ITS Backend

Currently, the lint rules used are as follows:

- `Pyflakes` (F)
- Subset of `pycodestyle` errors (E)
- `isort` (I)
- `pep8-naming` (N)
- `flake8-bugbear` (B)
- `flake8-builtins` (A)
- Subset of `flake8-django` (DJ)
- `flake8-return` (RET)

You can see the documentation of each [here](https://docs.astral.sh/ruff/rules/).

### Configure `ruff` Behavior

`ruff` configuration is laid out inside the [`ruff.toml`](./ruff.toml) file.

To add more lint errors, you can add full rule codes (e.g., `F401`) or any valid prefix (e.g., `F`) to the end of the `select` list.

You can find out more configurations [here](https://docs.astral.sh/ruff/configuration/).

## Debug

- set `DEBUG=TRUE` in `settings.py`

- The typical usage to break into the debugger is to insert
  - `import pdb; pdb.set_trace()` or
  - `breakpoint()`
