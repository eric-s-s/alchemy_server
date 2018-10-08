
./create_test_data.sh

mysql zoo -u zoo_guest  -e 'select * from zoo;'

mysql zoo -u zoo_guest  -e 'select * from monkey;'


# GET
printf "\n\n\ncommand: GET monkeys\n\n" | tee  output.txt  error.txt
curl localhost:8080/monkeys/ | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoos\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/ | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoo name wacky zachy\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/Wacky%20Zachy%27s%20Monkey%20Attacky | python3 -m json.tool >> output.txt 2>> error.txt


printf "\n\n\ncommand: GET monkey_id 2\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/monkeys/2 | python3 -m json.tool >> output.txt 2>> error.txt


printf "\n\n\ncommand: GET zoo via monkey_id 2\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/monkeys/2/zoo | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoo  ERROR\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/nope >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoo via monkey_id 2 ERROR\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/monkeys/100/zoo >> output.txt 2>> error.txt

# POST
printf "\n\n\ncommand POST zoo \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X POST -d\
     "{\"name\": \"Eric's Zoo Of Death\", \"opens\": \"05:00\", \
      \"closes\": \"14:00\"}" \
     localhost:8080/zoos/ | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand POST monkey \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X POST -d\
     "{\"name\": \"Bobo\", \"sex\": \"m\", \"flings_poop\": \"FALSE\",  \
      \"poop_size\": \"10\", \"zoo_name\": \"Eric's Zoo Of Death\"}" \
     localhost:8080/monkeys/ | python3 -m json.tool >> output.txt 2>> error.txt

# PUT
printf "\n\n\ncommand PUT zoo: FULL \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X PUT -d\
     "{\"opens\": \"6:30\", \"closes\": \"16:30\"}" \
     localhost:8080/zoos/Eric%27s%20Zoo%20Of%20Death | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand PUT monkey: FULL \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X PUT -d\
     "{\"name\": \"New Name\", \"flings_poop\": \"FALSE\",  \
      \"poop_size\": \"1000\", \"zoo_name\": \"Eric's Zoo Of Death\"}" \
     localhost:8080/monkeys/1 | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand PUT zoo: PARIAL \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X PUT -d\
     "{\"closes\": \"16:50\"}" \
     localhost:8080/zoos/Eric%27s%20Zoo%20Of%20Death | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand PUT monkey: PARTIAL \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X PUT -d\
     "{\"flings_poop\": \"TRUE\",  \
       \"zoo_name\": \"The Boringest Zoo On Earth\"}" \
     localhost:8080/monkeys/1 | python3 -m json.tool >> output.txt 2>> error.txt

# HEAD

printf "\n\n\ncommand HEAD zoos \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/zoos/ >> output.txt 2>> error.txt

printf "\n\n\ncommand HEAD monkeys \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/monkeys/ >> output.txt 2>> error.txt

printf "\n\n\ncommand HEAD zoos/wacky zachy \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/zoos/Wacky%20Zachy%27s%20Monkey%20Attacky >> output.txt 2>> error.txt

printf "\n\n\ncommand HEAD monkey/1 \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/monkeys/1 >> output.txt 2>> error.txt

printf "\n\n\ncommand HEAD monkeys/1/zoo \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/monkeys/1/zoo >> output.txt 2>> error.txt


printf "\n\n\ncommand HEAD specific zoo not there \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/zoos/nope >> output.txt 2>> error.txt


# DELETE

printf "\n\n\ncommand delete monkey #1\n\n" | tee  -a output.txt  error.txt
curl -X DELETE localhost:8080/monkeys/1 | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand delete wacky zachy's\n\n" | tee  -a output.txt  error.txt
curl -X DELETE localhost:8080/zoos/Wacky%20Zachy%27s%20Monkey%20Attacky | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand delete all monkeys\n\n" | tee  -a output.txt  error.txt
curl -X DELETE localhost:8080/monkeys/ | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoos\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/ | python3 -m json.tool >> output.txt 2>> error.txt

./create_test_data.sh

printf "\n\n\nREPOPULATING DB\n\n" | tee -a output.txt  error.txt

printf "\n\n\ncommand: GET monkeys\n\n" | tee -a output.txt  error.txt
curl localhost:8080/monkeys/ | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoos\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/ | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand delete all zoos\n\n" | tee  -a output.txt  error.txt
curl -X DELETE localhost:8080/zoos/ | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET monkeys\n\n" | tee -a output.txt  error.txt
curl localhost:8080/monkeys/ | python3 -m json.tool >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoos\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/ | python3 -m json.tool >> output.txt 2>> error.txt

