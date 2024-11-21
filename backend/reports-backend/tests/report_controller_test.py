import json
from unittest.mock import MagicMock

import pytest
from flask import Flask

from src.controllers.report_controller import init_report_routes


@pytest.fixture
def app(mock_report_repo):
    app = Flask(__name__, template_folder="../templates")
    app.testing = True
    init_report_routes(app, mock_report_repo)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_report_repo():
    return MagicMock()


def test_list_reports(client, mock_report_repo):
    mock_report_repo.list.return_value = [
        {"ID": 1, "REPORT_DATE": "2024-11-20", "REPORT_JSON": '{"key": "value"}'}
    ]
    response = client.get('/api/reports')
    assert response.status_code == 200
    assert response.json == [
        {"ID": 1, "REPORT_DATE": "2024-11-20", "REPORT_JSON": '{"key": "value"}'}
    ]
    mock_report_repo.list.assert_called_once()


def test_add_report(client, mock_report_repo):
    test_report = {"key": "value"}
    mock_report_repo.add.return_value = None
    response = client.post(
        '/api/reports',
        data=json.dumps(test_report),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "OK"
    mock_report_repo.add.assert_called_once_with(json.dumps(test_report))


def test_show_reports(client, mock_report_repo):
    mock_report_repo.list.return_value = [
        {"ID": 1, "REPORT_DATE": "2024-11-20", "REPORT_JSON": '{}'}
    ]
    response = client.get('/reports')
    data = str(response.data)
    assert response.status_code == 200
    assert "<!doctype html>" in data
    assert "2024-11-20" in data
    mock_report_repo.list.assert_called_once()


def test_show_report(client, mock_report_repo, app):
    report_id = 1

    app.add_url_rule('/show_videos', endpoint='show_videos', view_func=lambda: "Video Page")
    mock_report_repo.get.return_value = {
        "ID": report_id,
        "REPORT_DATE": "2024-11-20",
        "REPORT_JSON": '{"foo": "bar"}'
    }

    response = client.get(f'/reports/{report_id}')

    data = str(response.data)
    assert response.status_code == 200
    assert "<!doctype html>" in data
    assert "foo" in data
    assert "bar" in data
    mock_report_repo.get.assert_called_once_with(report_id)
