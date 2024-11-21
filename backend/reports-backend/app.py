import json

from flask import Flask, request, jsonify, render_template

import src.report as report_repo

app = Flask(__name__, static_folder="templates/assets")


@app.route('/api/reports', methods=['GET'])
def list_reports():
    return jsonify(report_repo.list())


@app.route('/api/reports', methods=['POST'])
def add_report():
    report = request.json
    report_repo.add(json.dumps(report))
    return "OK"


@app.route("/reports", methods=['GET'])
def show_reports():
    reports = report_repo.list()
    return render_template('reports.html', reports=reports)


@app.route("/reports/<int:report_id>", methods=['GET'])
def show_report(report_id: int):
    report = report_repo.get(report_id)
    return render_template('report.html', report=report)


if __name__ == '__main__':
    report_repo.init_table()
    app.run(debug=True)
