# Create and start a netsim network with devices specified in <lab>/netsim/,
# killing any running netsim instances:
# - one device per file
# - device name equals file name
# - file contains NED name

SIMDIR="$LABDIR/netsim"

if [ -d "$LAB/netsim" ]; then
	echo "Adding netsim devices"
	mkdir -p $SIMDIR

	CMD='create-device'
	for dev in `ls $LAB/netsim | sort || true`; do
		if [ -n "$DEBUG" ]; then echo "  $dev"; fi
		ncs-netsim --dir $SIMDIR $CMD "`cat $LAB/netsim/$dev`" $dev >/dev/null
		CMD='add-device'
	done

	echo "Restarting netsim"
	pkill -x confd || true
	ncs-netsim --dir $SIMDIR start >/dev/null

	if $ADDSIMDEVS; then
		ncs-netsim --dir $SIMDIR ncs-xml-init >$LABDIR/ncs-cdb/_netsim.xml
	fi
fi
