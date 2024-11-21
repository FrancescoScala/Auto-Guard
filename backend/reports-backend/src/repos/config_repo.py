import sqlite3


def __execute(stmt, param=None, needs_commit=False):
    db = sqlite3.connect('CONFIG_db.sqlite3')
    cursor = db.cursor()
    try:
        if param is None:
            cursor.execute(stmt)
        else:
            cursor.execute(stmt, param)
        records = cursor.fetchall()
        if needs_commit:
            db.commit()
        return records
    finally:
        cursor.close()
        db.close()


def init_table():
    __execute("""
        CREATE TABLE IF NOT EXISTS "CONFIG" (
            "ID"    INTEGER,
            "CONFIG_DATE"    TEXT NOT NULL,
            "CONFIG_JSON"    TEXT NOT NULL,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
    """)


def get(config_id):
    record = __execute(f"SELECT ID, CONFIG_DATE, CONFIG_JSON  FROM CONFIG WHERE ID = ?", param=(config_id,))
    report = dict(zip(["ID", "CONFIG_DATE", "CONFIG_JSON"], record[0]))
    return report


def get_latest():
    record = __execute(f"SELECT ID, CONFIG_DATE, CONFIG_JSON  FROM CONFIG ORDER BY ID DESC LIMIT 1")
    if len(record) > 0:
        report = dict(zip(["ID", "CONFIG_DATE", "CONFIG_JSON"], record[0]))
        return report
    else:
        return None


def list():
    records = __execute("SELECT ID, CONFIG_DATE, CONFIG_JSON FROM CONFIG ORDER BY ID DESC")
    records = [dict(zip(["ID", "CONFIG_DATE", "CONFIG_JSON"], record)) for record in records]
    return records


def add(config):
    records = __execute("INSERT INTO CONFIG (CONFIG_DATE, CONFIG_JSON) VALUES (CURRENT_TIMESTAMP, ?)",
                        param=(config,), needs_commit=True)
    return records


init_table()
