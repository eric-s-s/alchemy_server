export FLASK_APP=zoo_server/flask_app.py
export APP_CONFIG=../app_docker_config.cfg

flask run --host='0.0.0.0' --port=8080

