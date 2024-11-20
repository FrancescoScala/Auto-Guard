from flask import Flask, request, jsonify, render_template

from report import ReportRepo
import json

app = Flask(__name__, static_folder="templates/assets")



@app.route('/echo', methods=['POST'])
def hello():
    repo = ReportRepo()
    return jsonify(request.json)

@app.route('/api/reports', methods=['GET'])
def list_reports():
    repo = ReportRepo()
    return jsonify(repo.list())

@app.route('/api/reports', methods=['POST'])
def add_report():
    report = request.json
    repo = ReportRepo()
    repo.add(json.dumps(report))
    return "OK"


@app.route("/reports", methods=['GET'])
def show_reports():
    repo = ReportRepo()
    reports = repo.list()
    return render_template('reports.html', reports=reports)


@app.route("/reports/<int:report_id>", methods=['GET'])
def show_report(report_id: int):
    repo = ReportRepo()
    report = repo.get(report_id)
    return render_template('report.html', report=report)


if __name__ == '__main__':
    app.run(debug=True)
