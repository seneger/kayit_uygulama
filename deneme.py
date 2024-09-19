import pymysql

baglanti = pymysql.connect(
    host="localhost",
    user="root",
    password="Sngr2516.",
    db="sakila",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)
