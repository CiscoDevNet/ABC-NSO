init_common

echo "Setting up TIG stack in Docker"
cwd=$(pwd)
cd ${LAB}/tig
docker-compose up -d
cd ${cwd}
