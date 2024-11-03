import pyodbc
from config import Config

def test_sql_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={Config.SQL_SERVER};"
        f"DATABASE={Config.SQL_DATABASE};"
        f"UID={Config.SQL_USERNAME};"
        f"PWD={Config.SQL_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "connection timeout=30;"
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        print(f"Connection successful! SQL Server version: {row[0]}")
        conn.close()
        return True
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return False

if __name__ == "__main__":
    test_sql_connection() 