import mysql.connector
from mysql.connector import Error
from util.db_property_util import DBPropertyUtil

class DBConnUtil:
    _connection = None  # class-level cached connection

    @staticmethod
    def get_connection():
        if DBConnUtil._connection is not None and DBConnUtil._connection.is_connected():
            return DBConnUtil._connection

        try:
            # Load properties from db.properties
            props = DBPropertyUtil.get_connection_string("d:\\Transport_Management\\util\\db.properties")

            # Create connection using loaded properties
            DBConnUtil._connection = mysql.connector.connect(
                host=props["host"],
                port=int(props["port"]),
                user=props["user"],
                password=props["password"],
                database=props["database"]
            )

            if DBConnUtil._connection.is_connected():
                print("✅ Database connection successful!")
                return DBConnUtil._connection

        except Error as e:
            print(f"❌ Error while connecting to DB: {e}")

        return None

# Optional: Test connection
if __name__ == "__main__":
    conn = DBConnUtil.get_connection()
    if conn and conn.is_connected():
        conn.close()
