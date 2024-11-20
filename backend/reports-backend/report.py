class ReportRepo:
    repo: dict[int, object] = {}
    highest_id = 0

    def list(self):
        return self.repo

    def add(self, report: object):
        self.highest_id = self.highest_id + 1
        self.repo[self.highest_id] = report