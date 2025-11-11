import mysql.connector  
from mysql.connector import Error  

# تأكد من استبدال هذه القيم ببيانات اعتماد قاعدة البيانات الخاصة بك  
DB_CONFIG = {  
    'host': 'localhost',  # أو عنوان IP لخادم MySQL الخاص بك  
    'user': 'your_mysql_user',  
    'password': 'your_mysql_password',  
    'database': 'nfc_attendance_db' # اسم قاعدة البيانات التي تريد إعادة تعيينها  
}  

def reset_mysql_database(db_config):  
    database_name = db_config['database']  
    # نحتاج للاتصال بدون تحديد قاعدة بيانات في البداية لحذفها  
    db_config_no_db = db_config.copy()  
    del db_config_no_db['database']  

    connection = None  
    try:  
        # الاتصال بخادم MySQL بدون قاعدة بيانات محددة  
        connection = mysql.connector.connect(**db_config_no_db)  
        if connection.is_connected():  
            cursor = connection.cursor()  

            print(f"Attempting to drop database: {database_name}")  
            # تعطيل فحص المفاتيح الأجنبية مؤقتًا للسماح بالحذف  
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  
            cursor.execute(f"DROP DATABASE IF EXISTS {database_name};")  
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  
            print(f"Database '{database_name}' dropped successfully (if it existed).")  

            print(f"Attempting to create database: {database_name}")  
            cursor.execute(f"CREATE DATABASE {database_name};")  
            print(f"Database '{database_name}' created successfully.")  

    except Error as e:  
        print(f"Error while connecting to MySQL or resetting database: {e}")  
    finally:  
        if connection and connection.is_connected():  
            cursor.close()  
            connection.close()  
            print("MySQL connection closed.")  

if __name__ == "__main__":  
    # !!! تأكد من تحديث 'user' و 'password' و 'database' أعلاه !!!  
    reset_mysql_database(DB_CONFIG)