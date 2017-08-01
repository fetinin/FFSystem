from main import hello_world


def test_hello_route(flask_app):
    with flask_app.app_context():
        assert hello_world() == 'Hello World!'


