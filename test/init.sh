init_common
ncs_cmd -c "get /devices/device{router-core-B}/config/hostname" \
	| grep core-b >/dev/null && echo "Test PASS"
