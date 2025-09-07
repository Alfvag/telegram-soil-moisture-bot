from dotenv import load_dotenv
import pyodbc
import os

load_dotenv()

def get_connection():
    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_NAME", "")
    user = os.getenv("DB_USER", "")
    password = os.getenv("DB_PASSWORD", "")

    connection_string = (
        "DRIVER=MySQL ODBC 9.4 ANSI Driver;" +
        f"SERVER={server};" +
        f"DATABASE={database};" +
        f"UID={user};" +
        f"PWD={password};" +
        "charset=utf8mb4;"
    )

    return pyodbc.connect(str(connection_string))

def query_data():
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT plant_name, moisture, timestamp FROM moisturelog")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        print("Error querying data:", e)
        return []
    finally:
        conn.close()

def add_subscriber(chat_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subscribers (chat_id) VALUES (?)", (str(chat_id),))
        conn.commit()
        return True
    except pyodbc.Error as e:
        print("Error querying data:", e)
        return False
    finally:
        conn.close()

def remove_subscriber(chat_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscribers WHERE chat_id = ?", (str(chat_id),))
        conn.commit()
        
        row = cursor.rowcount
        if (row < 1 or not row):
            return False
        else:
            return True

    except pyodbc.Error as e:
        print("Error querying data:", e)
        return False
    finally:
        conn.close()

def is_subscriber(chat_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM subscribers WHERE chat_id = ?", (str(chat_id)))
        row = cursor.fetchone()

        if not row:
            return False
        else:
            return True
    except pyodbc.Error as e:
        print("Error querying data:", e)
        return False
    finally:
        conn.close()

def get_subscribers():
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM subscribers")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        print("Error querying data:", e)
        return []
    finally:
        conn.close()