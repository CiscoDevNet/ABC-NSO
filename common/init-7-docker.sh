# Prune the Docker system

echo "Pruning Docker system"
docker stop $(docker ps -aq)
docker rm -f $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker system prune -a -f
