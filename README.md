# alchemy server

## a copy of zoo server but using sqlAlchemy instead of straight mysql

Makes a zoo db that can be manipulated with curl


to run:

in the top directory for the project, you can run two ways:

```bash
$ export FLASK_APP=alchemy_server/flask_app.py
$ flask run --port=8080
```

or 
```bash
$ python -m zoo_server.flask_app
```

from the same top directory, you can run
```bash
$ ./curl_commands.sh
```
to load test data and see results of sample curl commands

stout > output.txt

sterr > error.txt


`GET` examples:

```bash
$ curl localhost:8080/zoos
$ curl localhost:8080/zoos/<name>

$ curl localhost:8080/zoos/<name>/<field - monkeys, opens, closes>

$ curl localhost:8080/monkeys  -> returns all jsons
$ curl localhost:8080/monkeys/<ID>
$ curl localhost:8080/mnonkeys/<ID>/<field - name, sex, flings_poop, poop_size, zoo_name

```

`DELETE` can delete zoos, zoo/name, monkeys, monkeys/id

`PUT` (update) -> only fields you are updating

`POST` (new) -> all fields required

```bash
$ curl -H "content-Type: application/json" -X POST -d \
"{\"name\": \"Eric's zoo of death\", \"opens\": \"05:00\", \
\"closes\": \"14:00\"}" \
localhost:8080/zoos/

$ curl -H "content-Type: application/json" -X POST -d\
"{\"name\": \"Bobo\", \"sex\": \"m\", \"flings_poop\": \
\"TRUE\",\"poop_size\": 100, \"zoo_name\": \"Eric's zoo of death\"}" \
localhost:8080/monkeys/

$ curl -H "content-Type: application/json" -X PUT -d\
'{"opens": "08:00"}'\
localhost:8080/zoos/Eric%27s%20zoo%20of%20death

$ curl -H "content-Type: application/json" -X PUT -d\
'{"name": "Anything But Bobo", "flings_poop": FALSE}'\ 
localhost:8080/monkeys/4  # the id of the monkey formerly known as Bobo
```

