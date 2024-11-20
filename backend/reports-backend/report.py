from flask_restful import Resource

class Report:
    def __init__(self, report_id: int, data):
        self.report_id = report_id
        self.data = data

class ReportRepo:
    repo: dict[int, Report] = {}
    highest_id = 0

    def list(self):

    def add(self, report: Report):
        self.highest_id = self.highest_id + 1
        self.repo[self.highest_id] = report

class ReportsResource(Resource):
    report_repo = ReportRepo()

    def get(self):
        return self.repo

    def post(self, report: Report):

