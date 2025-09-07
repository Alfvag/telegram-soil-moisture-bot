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
        cursor.execute("SELECT * FROM moisturelog")
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        print("Error querying data:", e)
        return []
    finally:
        conn.close()

def add_subscriber(chat_id):
    pass

def remove_subscriber(chat_id):
    pass

def get_subscribers():
    pass

if __name__ == "__main__":
    print(pyodbc.drivers())

    data = query_data()
    for row in data:
        print(row)