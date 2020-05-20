from chatbot.webex_teams_bot import flask_app

def test_incorrect_http_method():
    response = flask_app.test_client().get('/webex-teams/webhook')
    assert response.status_code == 405

def test_incorrect_http_path():
    response = flask_app.test_client().post('/incorrect-path')
    assert response.status_code == 404

