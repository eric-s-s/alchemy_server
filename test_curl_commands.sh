eval "$(./export_db_values)"

echo creating test data
cd sql_scripts
./load_test_data.sh
cd ..


mysql ${db} -u ${user}  -e 'select * from zoo;'

mysql ${db} -u ${user} -e 'select * from monkey;'


# GET
printf "\n\n\ncommand: GET monkeys\n\n" | tee  output.txt  error.txt
curl localhost:8080/monkeys/ | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoos\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/ | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoo name wacky zachy\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/1 | jq . >> output.txt 2>> error.txt


printf "\n\n\ncommand: GET monkey_id 2\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/monkeys/2 | jq . >> output.txt 2>> error.txt


printf "\n\n\ncommand: GET zoo via monkey_id 2\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/monkeys/2/zoo | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoo  ERROR\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/nope >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoo via monkey_id 2 ERROR\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/monkeys/100/zoo >> output.txt 2>> error.txt

# POST
printf "\n\n\ncommand POST zoo \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X POST -d\
     "{\"name\": \"Eric's Zoo Of Death\", \"opens\": \"05:00\", \
      \"closes\": \"14:00\"}" \
     localhost:8080/zoos/ | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand POST monkey \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X POST -d\
     "{\"name\": \"Bobo\", \"sex\": \"m\", \"flings_poop\": \"FALSE\",  \
      \"poop_size\": \"10\", \"zoo_id\": \"2\"}" \
     localhost:8080/monkeys/ | jq . >> output.txt 2>> error.txt

# PUT
printf "\n\n\ncommand PUT zoo: FULL \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X PUT -d\
     "{\"opens\": \"6:30\", \"closes\": \"16:30\"}" \
     localhost:8080/zoos/1 | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand PUT monkey: FULL \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X PUT -d\
     "{\"name\": \"New Name\", \"flings_poop\": \"FALSE\",  \
      \"poop_size\": \"1000\", \"zoo_id\": \"2\"}" \
     localhost:8080/monkeys/1 | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand PUT zoo: PARIAL \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X PUT -d\
     "{\"closes\": \"16:50\"}" \
     localhost:8080/zoos/1 | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand PUT monkey: PARTIAL \n\n" | tee  -a output.txt  error.txt
curl -H "content-Type: application/json" -X PUT -d\
     "{\"flings_poop\": \"TRUE\",  \
       \"zoo_id\": \"2\"}" \
     localhost:8080/monkeys/1 | jq . >> output.txt 2>> error.txt

# HEAD

printf "\n\n\ncommand HEAD zoos \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/zoos/ >> output.txt 2>> error.txt

printf "\n\n\ncommand HEAD monkeys \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/monkeys/ >> output.txt 2>> error.txt

printf "\n\n\ncommand HEAD zoos/wacky zachy \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/zoos/1 >> output.txt 2>> error.txt

printf "\n\n\ncommand HEAD monkey/1 \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/monkeys/1 >> output.txt 2>> error.txt

printf "\n\n\ncommand HEAD monkeys/1/zoo \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/monkeys/1/zoo >> output.txt 2>> error.txt


printf "\n\n\ncommand HEAD specific zoo not there \n\n" | tee  -a output.txt  error.txt
curl -I localhost:8080/zoos/nope >> output.txt 2>> error.txt


# DELETE

printf "\n\n\ncommand delete monkey #1\n\n" | tee  -a output.txt  error.txt
curl -X DELETE localhost:8080/monkeys/1 | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand delete wacky zachy's\n\n" | tee  -a output.txt  error.txt
curl -X DELETE localhost:8080/zoos/1 | jq . >> output.txt 2>> error.txt

./create_test_data.sh

printf "\n\n\nREPOPULATING DB\n\n" | tee -a output.txt  error.txt

printf "\n\n\ncommand: GET monkeys\n\n" | tee -a output.txt  error.txt
curl localhost:8080/monkeys/ | jq . >> output.txt 2>> error.txt

printf "\n\n\ncommand: GET zoos\n\n" | tee  -a output.txt  error.txt
curl localhost:8080/zoos/ | jq . >> output.txt 2>> error.txt

