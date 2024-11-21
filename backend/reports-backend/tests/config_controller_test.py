import pytest
import json
from unittest.mock import MagicMock
from flask import Flask

from src.controllers.config_controller import init_config_controller

@pytest.fixture
def mock_config_repo():
    return MagicMock()

@pytest.fixture
def mock_mqtt_client():
    return MagicMock()

@pytest.fixture
def app(mock_mqtt_client, mock_config_repo):
    app = Flask(__name__, template_folder="../templates")
    app.testing = True
    init_config_controller(app, mqtt_client=mock_mqtt_client, config_repo=mock_config_repo)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_list_configs(client, app, mock_config_repo):
    mock_config_repo.list.return_value = [{"id": 1, "config": "sample"}]

    response = client.get('/api/configs')

    assert response.status_code == 200
    assert response.json == [{"id": 1, "config": "sample"}]
    mock_config_repo.list.assert_called_once()

def test_add_config(client, app, mock_config_repo, mock_mqtt_client):
    test_config = {"key": "value"}
    mock_config_repo.add.return_value = None

    response = client.post(
        '/api/configs',
        data=json.dumps(test_config),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data == b"OK"
    mock_config_repo.add.assert_called_once_with(json.dumps(test_config))
    mock_mqtt_client.publish_config.assert_called_once_with(json.dumps(test_config))

def test_get_config_view(client, app, mock_config_repo):
    mock_config_repo.get_latest.return_value = {"CONFIG_JSON": '{"foo": "bar"}'}

    response = client.get('/config')

    assert response.status_code == 200
    assert "foo" in str(response.data)
    assert "bar" in str(response.data)

    mock_config_repo.get_latest.assert_called_once()

def test_save_config_form(client, app, mock_config_repo, mock_mqtt_client):
    test_json = '{"key": "value"}'

    response = client.post('/config', data={"config_json": test_json})

    assert response.status_code == 302
    assert response.headers["Location"] == "/config"

    mock_config_repo.add.assert_called_once_with(test_json)
    mock_mqtt_client.publish_config.assert_called_once_with(test_json)
