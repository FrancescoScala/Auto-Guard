from flask import Flask

import src.controllers.config_controller as config_controller
import src.controllers.report_controller as report_controller
import src.controllers.video_controller as video_controller
from src.mqtt_client import MqttClient

app = Flask(__name__, static_folder="templates/assets")
mqtt_client = MqttClient()
video_controller.init_video_controller(app)
config_controller.init_config_controller(app, mqtt_client)
report_controller.init_report_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
