echo "Copying TIG bootstrap files"
mkdir -p ${HOME}/tig
cp -r ${LAB}/tig/* ${HOME}/tig

init_common

echo "Setting up TIG stack in Docker"
cwd=$(pwd)
cd ${HOME}/tig
docker-compose up -d
cd ${cwd}
