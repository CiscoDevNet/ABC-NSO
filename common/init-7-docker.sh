# Prune the Docker system

echo "Pruning Docker system"
docker stop $(docker ps -aq) >/dev/null 2>&1 || exit 0
docker rm -f $(docker ps -aq) >/dev/null 2>&1 || exit 0
docker rmi $(docker images -q) >/dev/null 2>&1 || exit 0
docker volume rm $(docker volume ls -q) >/dev/null 2>&1 || exit 0
docker system prune -a -f >/dev/null 2>&1 || exit 0
