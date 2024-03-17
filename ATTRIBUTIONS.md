# Attributions

## Django Database Migrations

- pattern: `**/migrations/000*_*.py`

- Reference (where code comes from)

    - Django creates migration files everytime the `makemigrations` command is run to keep track of changes made upon the database schema used

- Reason for inclusion:

    - It keeps track of all the changes and migrations made on the database models

    - It helps multiple developers use a common database schema when developing the app and prevent them from committing conflicting changes to the database models

    - See more detailed reasons here:

        - [Blog: Should you Commit Django Migrations to Git?](https://paulonteri.com/thoughts/should-you-commit-migrations)
        - [Stack Overflow: Should I be adding the Django migration files in the .gitignore file?](https://stackoverflow.com/questions/28035119/should-i-be-adding-the-django-migration-files-in-the-gitignore-file)

## Miscellaneous Django Files

- Files:

    - [`manage.py`](./manage.py)
    - [`its_backend/asgi.py`](./its_backend/asgi.py)
    - [`its_backend/wsgi.py`](./its_backend/wsgi.py)

- Reference (where code comes from)

    - Automatically created by Django when first starting a Django project

- Reason for inclusion:

    - `manage.py` manages all the CLI commands Django provides, such as

        - `runserver` to start the Django server
        - `makemigrations` to create migration files for the DB model
        - `migrate` to make the migrations to the DB
        - etc.

    - `asgi.py` and `wsgi.py` serve as entry points for ASGI and WSGI servers respectively
