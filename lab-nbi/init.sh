echo "Installing required modules"
pip install pyats genie ncclient requests

init_common

echo "Creating a working directory"
mkdir -p $LABDIR/working-directory

echo "Copying a script skeleton"
cp $LAB/init/* $LABDIR/working-directory/
