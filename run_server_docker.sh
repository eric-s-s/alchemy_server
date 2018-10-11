#!/usr/bin/env bash
export FLASK_APP=zoo_server/flask_app.py
export APP_CONFIG=../flask_config_for_docker.cfg

flask run --host='0.0.0.0' --port=8080

