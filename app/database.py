import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'stock_portfolio')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def init_db():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create portfolio table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS portfolio (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    symbol VARCHAR(10) NOT NULL,
                    shares FLOAT NOT NULL,
                    purchase_price FLOAT NOT NULL,
                    purchase_date DATE NOT NULL
                )
            """)
            
            connection.commit()
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            connection.close()