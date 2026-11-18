import os
import oracledb
from dotenv import load_dotenv

load_dotenv()


user = os.getenv("COALA_USER")
password = os.getenv("COALA_PASSWORD")
dsn = os.getenv("COALA_DSN")

if not user or not password or not dsn:
    raise ValueError("Oracle credentials or DSN are missing.")

try:
    with oracledb.connect(
        user=user,
        password=password,
        dsn=dsn
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute("SELECT USER, SYS_CONTEXT('USERENV', 'CON_NAME') FROM dual")
            result = cursor.fetchone()

            print("Connection successful!")
            print("User:", result[0])
            print("Container:", result[1])

except oracledb.Error as error:
    print("Oracle connection failed:")
    print(error)