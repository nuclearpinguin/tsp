from app.app_factory import create_app

app = create_app(dict())
app.run_server(debug=True, port=8050)
