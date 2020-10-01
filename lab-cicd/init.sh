echo "Installing required modules"
pip install pyats genie ncclient requests

echo "Creating nso-iac directory"
mkdir -p ${HOME}/nso-iac
cp -r ${LAB}/init/* ${HOME}/nso-iac

init_common

echo "Spinning up GitLab-CE"
cwd=$(pwd)
cd ${LAB}/gitlab
make
cd ${cwd}

