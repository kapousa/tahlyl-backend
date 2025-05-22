import sqlite3
import mysql.connector

def map_sqlite_to_mysql_type(sqlite_type):
    sqlite_type = sqlite_type.upper()
    if "INT" in sqlite_type:
        return "INT"
    elif "CHAR" in sqlite_type or "CLOB" in sqlite_type or "TEXT" in sqlite_type:
        return "VARCHAR(255)"
    elif "BLOB" in sqlite_type:
        return "BLOB"
    elif "REAL" in sqlite_type or "FLOA" in sqlite_type or "DOUB" in sqlite_type:
        return "DOUBLE"
    elif "NUM" in sqlite_type or "DEC" in sqlite_type:
        return "DECIMAL(10,2)"
    elif "BOOL" in sqlite_type:
        return "TINYINT(1)"
    elif "DATE" in sqlite_type or "TIME" in sqlite_type:
        return "DATETIME"
    else:
        return "VARCHAR(255)"

# Connect to SQLite
sqlite_conn = sqlite3.connect('your_sqlite.db')
sqlite_cursor = sqlite_conn.cursor()

# Connect to MySQL
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='youruser',
    password='yourpassword',
    database='yourdatabase'
)
mysql_cursor = mysql_conn.cursor()

sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table_name in tables:
    table_name = table_name[0]

    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    columns = sqlite_cursor.fetchall()
    col_defs = []
    primary_keys = []
    for col in columns:
        col_name = col[1]
        col_type = map_sqlite_to_mysql_type(col[2])
        pk = col[5]
        auto_increment = "AUTO_INCREMENT" if pk == 1 and col_type == "INT" else ""
        col_defs.append(f"`{col_name}` {col_type} {auto_increment}".strip())
        if pk == 1:
            primary_keys.append(f"`{col_name}`")
    if primary_keys:
        col_defs.append(f"PRIMARY KEY ({', '.join(primary_keys)})")
    create_stmt = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join(col_defs)});"
    mysql_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
    mysql_cursor.execute(create_stmt)

    # Copy data
    sqlite_cursor.execute(f"SELECT * FROM `{table_name}`")
    rows = sqlite_cursor.fetchall()
    if rows:
        placeholders = ','.join(['%s'] * len(rows[0]))
        insert_stmt = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
        for row in rows:
            mysql_cursor.execute(insert_stmt, row)

mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()
sqlite_cursor.close()
sqlite_conn.close()
