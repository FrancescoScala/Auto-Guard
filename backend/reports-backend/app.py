import json

from flask import Flask, request, jsonify, render_template, redirect, url_for

import src.config_repo as config_repo
import src.report_repo as report_repo
import src.mqtt_client as mqtt_client

app = Flask(__name__, static_folder="templates/assets")


# Reports API
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

# Config APIs
@app.route('/api/configs', methods=['GET'])
def list_configs():
    return jsonify(config_repo.list())


@app.route('/api/configs', methods=['POST'])
def add_config():
    config = request.json
    config_json = json.dumps(config)
    config_repo.add(config_json)
    mqtt_client.publish_config(config_json)
    return "OK"

@app.route('/config', methods=['GET'])
def get_config_view():
    config = config_repo.get_latest()
    config_json_loaded = json.loads(config['CONFIG_JSON'])
    config_json = json.dumps(config_json_loaded, indent=4)
    return render_template("config.html", config=config, config_json=config_json)

@app.route('/config', methods=['POST'])
def save_config_form():
    submitted_json = request.form.get("config_json", "")
    config_repo.add(submitted_json)
    mqtt_client.publish_config(submitted_json)
    return redirect(url_for("get_config_view"))


if __name__ == '__main__':
    report_repo.init_table()
    app.run(debug=True)
