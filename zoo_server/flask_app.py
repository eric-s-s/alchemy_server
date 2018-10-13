"""a server for my dummy db using flask"""
from functools import partial

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

from sqlalchemy import create_engine

from sqlalchemy.exc import OperationalError

from zoo_server import USER, DB
from zoo_server.data_base_session import data_base_session_scope, DataBaseSession

from zoo_server.db_request_handler import DBRequestHandler, BadId, BadData


app = Flask(__name__)
app.config.from_object('zoo_server.flask_app_default_config')
try:
    app.config.from_envvar('APP_CONFIG')
    print('using config:')
    print(app.config)
except RuntimeError:
    print('using default config')

app_engine = create_engine(
    "mysql://{}@{}/{}".format(USER, app.config.get('DB_HOST_NAME'), DB),
    encoding='latin1'
)

DataBaseSession.configure(bind=app_engine)


@app.route('/zoos/', methods=['POST', 'GET'])
def all_zoos():
    with data_base_session_scope() as session:
        db_request_handler = DBRequestHandler(session)
        method = _get_method()
        request_json = _get_json()

        actions = {
            'GET': partial(db_request_handler.get_all_zoos),
            'POST': partial(db_request_handler.post_zoo, request_json),
        }
        reply = actions[method]()

    return reply


@app.route('/monkeys/', methods=['POST', 'GET'])
def all_monkeys():
    with data_base_session_scope() as session:
        db_request_handler = DBRequestHandler(session)
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(db_request_handler.get_all_monkeys),
            'POST': partial(db_request_handler.post_monkey, request_json),
        }
        reply = actions[method]()
    return reply


@app.route('/zoos/<zoo_id>', methods=['PUT', 'GET', 'DELETE'])
def zoo_by_name(zoo_id):
    with data_base_session_scope() as session:
        db_request_handler = DBRequestHandler(session)
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(db_request_handler.get_zoo, zoo_id),
            'PUT': partial(db_request_handler.put_zoo, zoo_id, request_json),
            'DELETE': partial(db_request_handler.delete_zoo, zoo_id)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>', methods=['PUT', 'GET', 'DELETE'])
def monkey_by_id(monkey_id):
    with data_base_session_scope() as session:
        db_request_handler = DBRequestHandler(session)
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(db_request_handler.get_monkey, monkey_id),
            'PUT': partial(db_request_handler.put_monkey, monkey_id, request_json),
            'DELETE': partial(db_request_handler.delete_monkey, monkey_id)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>/zoo', methods=['GET'])
def zoo_by_monkey_id(monkey_id):
    with data_base_session_scope() as session:
        db_request_handler = DBRequestHandler(session)
        method = _get_method()

        actions = {
            'GET': partial(db_request_handler.get_zoo_by_monkey, monkey_id)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>/zoo/<field>', methods=['GET'])
def zoo_field_by_monkey_id(monkey_id, field):
    with data_base_session_scope() as session:
        db_request_handler = DBRequestHandler(session)
        method = _get_method()

        actions = {
            'GET': partial(db_request_handler.get_zoo_field_by_monkey, monkey_id, field)
        }
        reply = actions[method]()
    return reply


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    code = 400
    e_type = e.__class__.__name__
    text = e.args[0]
    title="bad request"
    return jsonify(error=code, title=title, error_type=e_type, text=text), code


@app.errorhandler(OperationalError)
def handle_db_not_responding(e):
    code = 500
    e_type = e.__class__.__name__
    text = e.args[0]
    title="db trouble"
    return jsonify(error=code, title=title, error_type=e_type, text=text), code


@app.errorhandler(404)
def handle_not_found(e):
    return jsonify(error=404, title="not found", text=str(e)), 404


@app.errorhandler(BadId)
def handle_bad_id(e):
    code = 404
    e_type = e.__class__.__name__
    text = e.args[0]
    title="not found"
    return jsonify(error=code, title=title, error_type=e_type, text=text), code


@app.errorhandler(BadData)
def handle_bad_id(e):
    code = 400
    e_type = e.__class__.__name__
    text = e.args[0]
    title="bad request"
    return jsonify(error=code, title=title, error_type=e_type, text=text), code


def _get_json() -> dict:
    """
    :raise: BadRequest
    :rtype: dict
    :return: JSON as dict
    """
    try:
        return request.get_json()
    except BadRequest:
        msg = "This here is we call a fucked-up JSON: {}".format(request.data)
        raise BadRequest(msg)


def _get_method():
    method = request.method
    if method == 'HEAD':
        return 'GET'
    return method


if __name__ == '__main__':
    app.run()
