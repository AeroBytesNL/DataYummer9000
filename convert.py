import psycopg2
import mysql.connector

postgres_conn = psycopg2.connect(
    host="192.168.1.49",
    user="alldaybot",
    password="alldaybot",
    database="alldaybot"
)

mariadb_conn = mysql.connector.connect(
    host="192.168.1.47",
    user="alldaybot",
    password="yeet",
    database="alldaybot"
)

postgres_cur = postgres_conn.cursor()

if postgres_conn:
    print("Connected to PostgreSQL")
else:
    print("Failed to connect to PostgreSQL")

mariadb_cur = mariadb_conn.cursor()
if mariadb_conn:
    print("Connected to MariaDB")
else:
    print("Failed to connect to MariaDB")

mariadb_cur.execute("SELECT * FROM messages")
messages = mariadb_cur.fetchall()

for message in messages:
    postgres_cur.execute(
        "INSERT INTO messages VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
            message[0], message[1], message[2], message[3], message[4], message[5], message[6], message[7]
        )
    )
    postgres_conn.commit()
    print("Message inserted")