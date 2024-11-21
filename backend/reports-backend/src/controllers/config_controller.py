import json

from flask import Flask, request, jsonify, render_template, redirect, url_for

import src.mqtt_client as mqtt_client
import src.repos.config_repo as config_repo


def init_config_controller(app: Flask):
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
