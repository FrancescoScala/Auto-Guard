import sqlite3


def __execute(stmt, param=None, needs_commit=False):
    db = sqlite3.connect('report_db.sqlite3')
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
        CREATE TABLE IF NOT EXISTS "REPORT" (
            "ID"    INTEGER,
            "REPORT_DATE"    TEXT NOT NULL,
            "REPORT_JSON"    TEXT NOT NULL,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
    """)


def get(report_id):
    record = __execute(f"SELECT ID, REPORT_DATE, REPORT_JSON  FROM REPORT WHERE ID = ?", param=(report_id,))
    report = dict(zip(["ID", "REPORT_DATE", "REPORT_JSON"], record[0]))
    return report


def list():
    records = __execute("SELECT ID, REPORT_DATE, REPORT_JSON FROM REPORT ORDER BY ID DESC")
    records = [dict(zip(["ID", "REPORT_DATE", "REPORT_JSON"], record)) for record in records]
    return records


def add(report):
    records = __execute("INSERT INTO REPORT (REPORT_DATE, REPORT_JSON) VALUES (CURRENT_TIMESTAMP, ?)",
                        param=(report,), needs_commit=True)
    return records

init_table()
