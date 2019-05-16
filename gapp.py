from app.app_factory import create_app

app_ = create_app()
app = app_.server
