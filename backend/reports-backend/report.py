import json

from flask import request
from flask_restful import Resource

class ReportRepo:
    repo: dict[int, object] = {}
    highest_id = 0

    def list(self):
        return self.repo

    def add(self, report: object):
        self.highest_id = self.highest_id + 1
        self.repo[self.highest_id] = report


class ReportsResource(Resource):
    report_repo = ReportRepo()

    def get(self):
        return self.report_repo.list()

    def post(self):
        report = request.json
        self.report_repo.add(report)
        return "OK"
