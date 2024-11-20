from flask import Flask, request, jsonify
from report import ReportRepo
import json

app = Flask(__name__)



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


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 6002, debug=True)
