# Connect devices

runcli() {
	ERROR=`echo "$1 | begin XXXX" | ncs_cli -NCu admin`
	if [ "$ERROR" ]; then
		echo $ERROR
		exit 1
	fi
}

echo "Connecting to devices"
runcli "devices fetch-ssh-host-keys"

if [ -f "$LAB/push.list" ]; then
	for dev in `cat $LAB/push.list`; do
		echo "Pushing config to $dev"
		runcli "devices device $dev sync-to"
	done
fi

runcli "devices sync-from"
