echo "Installing required modules"
pip install pyats genie ncclient requests

echo "Spinning up GitLab-CE"
cd gitlab
make
cd ..

echo "Creating nso-iac directory"
mkdir -p ${HOME}/nso-iac
cp -r ${LAB}/init/* ${HOME}/nso-iac

init_common

