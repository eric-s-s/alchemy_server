'''a server for my dummy db using flask'''
from functools import partial
import sys 

from flask import Flask, request
from werkzeug.exceptions import BadRequest

from zoo_server.request_handler import safe_handler

app = Flask(__name__)


"""

cases:
GET
zoos/                   returns: name, opens, closes, number_of_monkeys
zoos/<name>             returns: name, opens, closes, monkeys

monkeys/                returns: id, name, sex, flings_poop, poop_size, zoo_name
monkeys/<id>            returns: id, name, sex, flings_poop, poop_size, zoo_name
monkeys/<id>/zoo        returns: as zoos/<name>

POST
zoos/                   json_field: name, opens, closes
monkeys/                json_field: name, sex, flings_poop, poop_size, zoo_name

PUT
zoos/<name>             possible fields: opens, closes, [monkey_ids] (adds to current)
monkeys/<id>            possible fields: name, flings_poop, poop_size, zoo_name  NOTE sex returns 404

DELETE
zoos/                   all zoos and their associated monkeys
monkeys/                all monkeys but not the zoos
zoos/<name>             zoo and all monkeys in the zoo
monkeys/<id>            just the one monkey

"""


@app.route('/zoos/', methods=['POST', 'GET', 'DELETE'])
def all_zoos():
    app_host = app.config.get('app_host')
    with safe_handler(app_host) as handler:
        method = _get_method()
        request_json = _get_json()

        actions = {
            'GET': partial(handler.get_all_zoos),
            'POST': partial(handler.post_zoo, request_json),
            'DELETE': partial(handler.delete_all_zoos)
        }
        reply = actions[method]()

    return reply


@app.route('/monkeys/', methods=['POST', 'GET', 'DELETE'])
def all_monkeys():
    app_host = app.config.get('app_host')
    with safe_handler(app_host) as handler:
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(handler.get_all_monkeys),
            'POST': partial(handler.post_monkey, request_json),
            'DELETE': partial(handler.delete_all_monkeys)
        }
        reply = actions[method]()
    return reply


@app.route('/zoos/<zoo_name>', methods=['PUT', 'GET', 'DELETE'])
def zoo_by_name(zoo_name):
    app_host = app.config.get('app_host')
    with safe_handler(app_host) as handler:
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(handler.get_single_zoo, zoo_name),
            'PUT': partial(handler.put_zoo, zoo_name, request_json),
            'DELETE': partial(handler.delete_single_zoo, zoo_name)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>', methods=['PUT', 'GET', 'DELETE'])
def monkey_by_id(monkey_id):
    app_host = app.config.get('app_host')
    with safe_handler(app_host) as handler:
        method = _get_method()

        request_json = _get_json()

        actions = {
            'GET': partial(handler.get_single_monkey, monkey_id),
            'PUT': partial(handler.put_monkey, monkey_id, request_json),
            'DELETE': partial(handler.delete_single_monkey, monkey_id)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>/zoo', methods=['GET'])
def zoo_by_monkey_id(monkey_id):
    app_host = app.config.get('app_host')
    with safe_handler(app_host) as handler:
        method = _get_method()

        actions = {
            'GET': partial(handler.get_zoo_by_monkey, monkey_id)
        }
        reply = actions[method]()
    return reply


@app.route('/monkeys/<monkey_id>/zoo/<field>', methods=['GET'])
def zoo_field_by_monkey_id(monkey_id, field):
    app_host = app.config.get('app_host')
    with safe_handler(app_host) as handler:
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
    host_arg = 'localhost'
    if len(sys.argv) > 1:
        host_arg = sys.argv[1]
    app.config['app_host'] = host_arg
    app.run(host="0.0.0.0", port=8080)

