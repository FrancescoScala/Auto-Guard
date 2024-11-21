import json
import os

import src.repos.report_repo as report_repo
from flask import Flask, request, jsonify, render_template


def init_report_routes(app: Flask):
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
        return render_template('reports.html', reports=reports, video_file=video_file)

    @app.route("/reports/<int:report_id>", methods=['GET'])
    def show_report(report_id: int):
        report = report_repo.get(report_id)
        report_data = json.loads(report['REPORT_JSON'])
        report_data = json.dumps(report_data, indent=4)
        return render_template('report.html', report=report, report_data=report_data)
