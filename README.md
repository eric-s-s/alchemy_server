# alchemy server

## a copy of zoo server but using sqlAlchemy instead of straight mysql

Makes a zoo db that can be manipulated with curl


to run:
 ```bash
$ ./run_server_default.sh
```


from the same top directory you can load test data and run it with:
```bash
$ ./curl_commands.sh
```
WARNING: THIS WILL ERASE ALL DATA FROM DATABASE ONLY USE FOR A TEST DATABASE

stout > output.txt

sterr > error.txt


`GET` examples:

```bash
$ curl localhost:8080/zoos/
$ curl localhost:8080/zoos/<id>

$ curl localhost:8080/zoos/<id>>

$ curl localhost:8080/monkeys/  -> returns all jsons
$ curl localhost:8080/monkeys/<ID>
$ curl localhost:8080/mnonkeys/<ID>

```

`DELETE` can delete zoo/id, monkeys/id

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
localhost:8080/zoos/3

$ curl -H "content-Type: application/json" -X PUT -d\
'{"name": "Anything But Bobo", "flings_poop": FALSE}'\ 
localhost:8080/monkeys/4  # the id of the monkey formerly known as Bobo
```

