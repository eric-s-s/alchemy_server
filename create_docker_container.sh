echo docker stop zoo_server1
docker stop zoo_server1
echo docker rm zoo_server1
docker rm zoo_server1
echo docker run --network=zoo_network --name=zoo_server1 --env-file=./docker_env.txt -p 8080:8080 -d zoo_server
docker run --network=zoo_network --name=zoo_server1 --env-file=./docker_env.txt -p 8080:8080 -d zoo_server

