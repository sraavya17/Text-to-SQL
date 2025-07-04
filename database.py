import os
from dotenv import load_dotenv
import mysql.connector

"""Load the environment variables from the .env file"""
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('db_host'),
    'user': os.getenv('db_user'),
    'password': os.getenv('db_password'),
    'database': os.getenv('db_name')
}

def database_connection():
    """Establish and return the database connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def database_schema():
    """Return the schema of the database as a string"""
    conn = None
    try:
        conn = database_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print("Tables in the database:", tables)
        schema_info = []
        for table in tables:
            cursor.execute(f'DESCRIBE {table}')
            columns = cursor.fetchall()
            schema_info.append(f"Table '{table}' : {columns}")
        return "\n".join(schema_info)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

def execute_query(query):
    """Execute a given SQL query and return the results"""
    conn = None
    try:
        conn = database_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            return {
                "status": "success",
                "data": results,
                "row count": cursor.rowcount
            }
        else:
            conn.commit()
            return {
                "status": "success",
                "rows affected": cursor.rowcount
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    schema = database_schema()
    print(schema)
    result = execute_query("INSERT INTO employees (employee_id, first_name, last_name, hourly_pay, hire_date)VALUES(6, 'Kiran', 'kumar', 20.00, '2023-10-01')")
    print(result)
    
    
