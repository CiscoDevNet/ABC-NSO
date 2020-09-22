cp ~/solution/*.py ~/nso-lab-actions/packages/l3vpn/python/l3vpn/
cp ~/solution/*.yang ~/nso-lab-actions/packages/l3vpn/src/yang/
make -C ~/nso-lab-actions/packages/l3vpn/src
echo 'packages reload' | ncs_cli -NCu admin
