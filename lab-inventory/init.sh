init_common

cd $LAB
ncs_load -l -m -u admin -p '/devices/device{dist-rtr01}/config/domain' cdb2/01-out-of-sync.xml
ncs_load -l -m -n -p '/devices/device{dist-rtr01}' cdb2/02-devices.xml

cp -f xr-snippet.txt $LABDIR/
cp -f lab2.py $LABDIR/
