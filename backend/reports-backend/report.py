
import sqlite3
from re import finditer
class ReportRepo(object):
    def __init__(self):
        self._db = sqlite3.connect('report_db.sqlite3')

    def __del__(self):
        self._db.close()

    def __execute(self, stmt, param = None):
        args = []



        cursor = self._db.cursor()
        if param is None:
            cursor.execute(stmt)
        else:
            cursor.execute(stmt, param)
        records = cursor.fetchall()
        cursor.close()
        return records


    repo: dict[int, object] = {}
    highest_id = 0

    def list(self):
        records = self.__execute("SELECT ID, REPORT_DATE, REPORT_JSON  FROM REPORT")
        records = [dict(zip(["ID", "REPORT_DATE", "REPORT_JSON"], record)) for record in records]
        return records

    def add(self, report):
        records = self.__execute("INSERT INTO REPORT (REPORT_DATE, REPORT_JSON) VALUES (CURRENT_TIMESTAMP, ?)",
                                 (report,))
        self._db.commit()
        return records