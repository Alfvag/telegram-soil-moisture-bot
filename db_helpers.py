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
    plants = get_plants()
    conn = get_connection()
    result = list()

    try:
        cursor = conn.cursor()

        for plant in plants:
            print(plant)

            cursor.execute("SELECT plant_name, moisture, timestamp FROM moisturelog WHERE plant_name = ? ORDER BY timestamp DESC LIMIT 24", (plant,))
            rows = cursor.fetchall()
            
            # Create a dictionary for this plant's data
            plant_data = {
                "plant_name": plant,
                "measurements": []
            }
            
            # Add each measurement to the plant's data
            for row in rows:
                measurement = {
                    "plant_name": row[0],
                    "moisture": row[1],
                    "timestamp": row[2]
                }
                plant_data["measurements"].append(measurement)
            
            # Add this plant's data to the result list
            result.append(plant_data)

        return result
    except pyodbc.Error as e:
        print("Error querying data:", e)
        return []
    finally:
        conn.close()

def get_plants():
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT plant_name FROM plants")
        rows = cursor.fetchall()

        result = list()

        for row in rows:
            result.append(row[0])

        return result
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