from flask import Flask, request, jsonify, render_template
from report import ReportRepo

app = Flask(__name__)

repo = ReportRepo()

@app.route('/echo', methods=['POST'])
def hello():
    return jsonify(request.json)

@app.route('/api/reports', methods=['GET'])
def list_reports():
    return jsonify(repo.list())

@app.route('/api/reports', methods=['POST'])
def add_report():
    report = request.json
    repo.add(report)
    return "OK"

@app.route("reports", methods=['GET'])
def show_reports():
    return render_template('templates.html', reports=repo.list())

if __name__ == '__main__':
    app.run(debug=True)
