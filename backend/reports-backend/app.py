from flask import Flask

import src.controllers.config_controller as config_controller
import src.controllers.report_controller as report_controller
import src.controllers.video_controller as video_controller
import src.repos.report_repo as report_repo
import src.repos.config_repo as config_repo
from src.mqtt_client import MqttClient

if __name__ == 'app' or __name__ == '__main__':
    app = Flask(__name__, static_folder="templates/assets")
    mqtt_client = MqttClient()

    video_controller.init_video_controller(app)
    config_controller.init_config_controller(app, mqtt_client, config_repo)
    report_controller.init_report_routes(app, report_repo)

    if __name__ == '__main__':
        app.run(debug=True)
