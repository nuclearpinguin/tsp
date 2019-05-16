from app.app_factory import create_app

app = create_app()
app.run_server(debug=True, port=8050, host='0.0.0.0')
