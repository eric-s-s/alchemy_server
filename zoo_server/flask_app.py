'''a server for my dummy db using flask'''
from functools import partial
import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

from zoo_server.db_request_handler import safe_db_handler


app = Flask(__name__)
app.config.from_object('zoo_server.flask_app_default_config')
try:
    app.config.from_envvar('APP_CONFIG')
    print('using config:')
    print(app.config)
except RuntimeError:
    print('using default config')


"""

cases:
GET
zoos/                   returns: id, name, opens, closes, monkeys
zoos/<id>               returns: id, name, opens, closes, monkeys

monkeys/                returns: id, name, sex, flings_poop, poop_size, zoo_name, zoo_id
monkeys/<id>            returns: id, name, sex, flings_poop, poop_size, zoo_name, zoo_id
monkeys/<id>/zoo        returns: as zoos/<id>

POST
zoos/                   json_field: name, opens, closes
monkeys/                json_field: name, sex, flings_poop, poop_size, zoo_id

PUT
zoos/<id>               possible fields: name, opens, closes, monkey_id (adds to current)
monkeys/<id>            possible fields: name, flings_poop, poop_size, zoo_id

DELETE
zoos/<id>               zoo and all monkeys in the zoo
monkeys/<id>            just the one monkey

"""


@app.route('/zoos/', methods=['POST', 'GET'])
def all_zoos():
    db_host_name = app.config.get('DB_HOST_NAME')
    with safe_db_handler(db_host_name) as handler:
        method = _get_method()
        request_json = _get_json()

        actions = {
            'GET': partial(handler.get_all_zoos),
            'POST': partial(handler.post_zoo, request_json),
        }
        reply = actions[method]()

    return reply


@app.route('/monkeys/', methods=['POST', 'GET'])
def all_monkeys():
    db_host_name = app.config.get('DB_HOST_NAME')
    with safe_db_handler(db_host_name) as handler:
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(handler.get_all_monkeys),
            'POST': partial(handler.post_monkey, request_json),
        }
        reply = actions[method]()
    return reply


@app.route('/zoos/<zoo_id>', methods=['PUT', 'GET', 'DELETE'])
def zoo_by_name(zoo_id):
    db_host_name = app.config.get('DB_HOST_NAME')
    with safe_db_handler(db_host_name) as handler:
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(handler.get_zoo, zoo_id),
            'PUT': partial(handler.put_zoo, zoo_id, request_json),
            'DELETE': partial(handler.delete_zoo, zoo_id)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>', methods=['PUT', 'GET', 'DELETE'])
def monkey_by_id(monkey_id):
    db_host_name = app.config.get('DB_HOST_NAME')
    with safe_db_handler(db_host_name) as handler:
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(handler.get_monkey, monkey_id),
            'PUT': partial(handler.put_monkey, monkey_id, request_json),
            'DELETE': partial(handler.delete_monkey, monkey_id)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>/zoo', methods=['GET'])
def zoo_by_monkey_id(monkey_id):
    db_host_name = app.config.get('DB_HOST_NAME')
    with safe_db_handler(db_host_name) as handler:
        method = _get_method()

        actions = {
            'GET': partial(handler.get_zoo_by_monkey, monkey_id)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>/zoo/<field>', methods=['GET'])
def zoo_field_by_monkey_id(monkey_id, field):
    db_host_name = app.config.get('DB_HOST_NAME')
    with safe_db_handler(db_host_name) as handler:
        method = _get_method()

        actions = {
            'GET': partial(handler.get_zoo_field_by_monkey, monkey_id, field)
        }
        reply = actions[method]()
    return reply


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
    app.run(host="localhost", port=8080)

