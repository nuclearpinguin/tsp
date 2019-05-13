from app.app_factory import create_app
from dash import Dash


class TestApp:
    app = create_app()

    def test_factory(self):
        assert isinstance(self.app, Dash)
        assert hasattr(self.app, 'run_server')

    def test_callback(self):
        callbacks = self.app.callback_map
        for k, v in callbacks.items():
            assert 'inputs' in v.keys()
            assert 'state' in v.keys()

