import sqlite3
import mysql.connector
import re


def map_sqlite_to_mysql_type(sqlite_type_raw, is_primary_key=False):
    """Maps SQLite data types to appropriate MySQL data types."""
    sqlite_type = sqlite_type_raw.upper()

    if "INT" in sqlite_type:
        if "TINYINT" in sqlite_type:
            return "TINYINT"
        elif "SMALLINT" in sqlite_type:
            return "SMALLINT"
        elif "MEDIUMINT" in sqlite_type:
            return "MEDIUMINT"
        elif "BIGINT" in sqlite_type:
            return "BIGINT"
        return "INT"
    elif "CHAR" in sqlite_type or "CLOB" in sqlite_type or "TEXT" in sqlite_type:
        # If it's a primary key and potentially a TEXT type, force VARCHAR with a reasonable length
        if is_primary_key:
            # Common length for IDs that are textual but not too long (e.g., UUIDs are 36 chars)
            # Adjust this length based on the actual data in your 'id' column in SQLite
            print(f"Warning: Primary Key '{sqlite_type_raw}' mapped to VARCHAR(255). Adjust if actual data is longer.")
            return "VARCHAR(255)"

        match = re.search(r'\((\d+)\)', sqlite_type_raw)
        if match:
            length = int(match.group(1))
            return f"VARCHAR({min(length, 255)})"  # Keep 255 for common cases, or 65535
        return "TEXT"  # For non-primary key TEXT columns, use MySQL's TEXT
    elif "BLOB" in sqlite_type:
        # If BLOB is a primary key, it's highly unusual and usually means something else
        # You'd typically use a VARBINARY with a length for binary IDs or hashes.
        if is_primary_key:
            print(f"Warning: BLOB Primary Key '{sqlite_type_raw}' mapped to VARBINARY(255). Adjust as needed.")
            return "VARBINARY(255)"
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
        print(f"Warning: Unknown SQLite type '{sqlite_type_raw}'. Defaulting to VARCHAR(255).")
        return "VARCHAR(255)"


def migrate_sqlite_to_mysql(sqlite_db_path, mysql_config):
    """
    Migrates a SQLite database to MySQL, including table schemas and data.
    """
    sqlite_conn = None
    mysql_conn = None
    sqlite_cursor = None
    mysql_cursor = None

    try:
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()
        print(f"Connected to SQLite database: {sqlite_db_path}")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return

    try:
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor()
        print(f"Connected to MySQL database: {mysql_config['database']}")
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        if sqlite_cursor: sqlite_cursor.close()
        if sqlite_conn: sqlite_conn.close()
        return

    try:
        mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        mysql_conn.commit()
        print("Disabled MySQL foreign key checks.")
    except mysql.connector.Error as err:
        print(f"Error disabling foreign key checks: {err}")

    try:
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = sqlite_cursor.fetchall()
        print(f"Found tables in SQLite: {[t[0] for t in tables]}")

        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            if table_name == 'sqlite_sequence':
                print(f"Skipping internal SQLite table: {table_name}")
                continue
            if table_name.startswith('sqlite_autoindex_'):
                print(f"Skipping internal SQLite autoindex table: {table_name}")
                continue

            print(f"\nProcessing table: `{table_name}`")

            sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
            columns = sqlite_cursor.fetchall()
            col_defs = []
            primary_keys = []

            # First pass to identify primary keys
            pk_col_names = {col[1] for col in columns if col[5] == 1}

            for col in columns:
                col_name = col[1]
                sqlite_type = col[2]
                not_null = col[3]
                default_value = col[4]
                pk = col[5]

                # Pass `is_primary_key` flag to the mapping function
                mysql_type = map_sqlite_to_mysql_type(sqlite_type, is_primary_key=(col_name in pk_col_names))

                auto_increment = ""
                # Ensure AUTO_INCREMENT is only applied to integer primary keys
                if pk == 1 and ("INT" in mysql_type or "BIGINT" in mysql_type):
                    auto_increment = " AUTO_INCREMENT"
                    if not_null == 0:
                        print(
                            f"Warning: Primary key '{col_name}' in table '{table_name}' is NULLABLE in SQLite. MySQL AUTO_INCREMENT implies NOT NULL.")
                    not_null_sql = " NOT NULL"
                elif not_null == 1:
                    not_null_sql = " NOT NULL"
                else:
                    not_null_sql = ""

                default_sql = ""
                if default_value is not None:
                    if isinstance(default_value, str) and (
                            "TEXT" in mysql_type or "VARCHAR" in mysql_type or
                            "DATE" in mysql_type or "TIME" in mysql_type
                    ):
                        default_sql = f" DEFAULT '{default_value}'"
                    else:
                        default_sql = f" DEFAULT {default_value}"

                col_defs.append(f"`{col_name}` {mysql_type}{not_null_sql}{default_sql}{auto_increment}".strip())
                if pk == 1:
                    primary_keys.append(f"`{col_name}`")

            if primary_keys:
                # For non-integer primary keys, MySQL requires a length if it's TEXT/BLOB
                # We handle this by mapping to VARCHAR/VARBINARY with a length directly in map_sqlite_to_mysql_type
                col_defs.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

            joined_col_defs = ',\n    '.join(col_defs)
            create_stmt = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n    {joined_col_defs}\n);"

            print(f"Generated CREATE TABLE statement:\n{create_stmt}")

            try:
                mysql_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
                mysql_cursor.execute(create_stmt)
                print(f"Table `{table_name}` created in MySQL.")
            except mysql.connector.Error as err:
                print(f"Error creating table `{table_name}`: {err}")
                continue

            sqlite_cursor.execute(f"SELECT * FROM `{table_name}`")
            rows = sqlite_cursor.fetchall()
            if rows:
                placeholders = ','.join(['%s'] * len(rows[0]))
                insert_stmt = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
                print(f"Copying {len(rows)} rows to `{table_name}`...")

                batch_size = 1000
                for i in range(0, len(rows), batch_size):
                    batch = rows[i:i + batch_size]
                    try:
                        mysql_cursor.executemany(insert_stmt, batch)
                    except mysql.connector.Error as err:
                        print(
                            f"Error inserting data into `{table_name}` (batch {i // batch_size}, starting row {i}): {err}")
                        mysql_conn.rollback()
                        break

                mysql_conn.commit()
                print(f"Data copied to `{table_name}`.")
            else:
                print(f"No data to copy for table `{table_name}`.")

    except Exception as e:
        print(f"An unexpected error occurred during migration: {e}")
        if mysql_conn:
            mysql_conn.rollback()

    finally:
        if mysql_cursor and mysql_conn:
            try:
                mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                mysql_conn.commit()
                print("\nForeign key checks re-enabled in MySQL.")
            except mysql.connector.Error as err:
                print(f"Error re-enabling foreign key checks: {err}")

        if mysql_cursor:
            mysql_cursor.close()
        if mysql_conn:
            mysql_conn.close()
        if sqlite_cursor:
            sqlite_cursor.close()
        if sqlite_conn:
            sqlite_conn.close()
        print("Database connections closed.")


# --- Configuration ---
sqlite_database_file = 'tahlyl-local-dbe.db'
mysql_connection_config = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12787513',
    'password': '4EfcfHXC4y',
    'database': 'sql12787513'
}

# --- Run the migration ---
if __name__ == "__main__":
    migrate_sqlite_to_mysql(sqlite_database_file, mysql_connection_config)


### Clean the DB ###
# USE your_database_name;
#
# SET FOREIGN_KEY_CHECKS = 0;
#
# SELECT CONCAT('DROP TABLE IF EXISTS `', table_name, '`;')
# FROM information_schema.tables
# WHERE table_schema = 'your_database_name' AND table_type = 'BASE TABLE';
#
# SET FOREIGN_KEY_CHECKS = 1;