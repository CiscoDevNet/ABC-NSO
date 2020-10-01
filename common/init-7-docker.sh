# Prune the Docker system

echo "Pruning Docker system"
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker system prune -a -f
