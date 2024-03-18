import os
import shutil
import signal
import sqlite3
import subprocess
import time

TEST = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TEST)
POSTMAN_COLLECTION = "ITS-API-Test.postman_collection.json"
SERVER_PID = None

DJ_MANAGE = os.path.join(ROOT, "manage.py")

ORIG_DB = os.path.join(ROOT, 'db.sqlite3')
TEMP_DB = os.path.join(TEST, 'temp.sqlite3')

def cleanup():
    if os.path.exists(TEMP_DB):
        shutil.move(TEMP_DB, ORIG_DB)
    if SERVER_PID:
        os.kill(SERVER_PID, signal.SIGTERM)

def populate_db():
    sql_script_file = os.path.join(TEST, "populate_db.sql")
    with open(sql_script_file, 'r') as f:
        sql_script = f.read()

    # Connect to the SQLite database
    connection = sqlite3.connect(ORIG_DB)
    cursor = connection.cursor()

    # Execute the SQL script
    cursor.executescript(sql_script)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

def main():
    global SERVER_PID

    try:
        # Backup original DB if it exists
        if os.path.exists(ORIG_DB):
            shutil.move(ORIG_DB, TEMP_DB)
        
        # Make and apply migrations
        subprocess.Popen(["python", DJ_MANAGE, "makemigrations"]).wait()
        subprocess.Popen(["python", DJ_MANAGE, "migrate"]).wait()

        # Populate DB with test data
        populate_db()

        # Run server in the background
        server_proc = subprocess.Popen(["python", DJ_MANAGE, "runserver"])
        SERVER_PID = server_proc.pid

        # Wait for server startup
        time.sleep(5)

        # Run postman tests
        postman_collection = os.path.join(TEST, POSTMAN_COLLECTION)
        subprocess.Popen(["newman", "run", postman_collection]).wait()
    except:  # noqa: E722
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    main()
