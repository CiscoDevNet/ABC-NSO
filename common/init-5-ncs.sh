# Start NSO instance, stopping the previous one if needed

CONF=""
if [ -f $LABDIR/ncs.conf ]; then
	CONF="-c $LABDIR/ncs.conf"
fi

echo "Restarting NSO in $LABDIR"
ncs --timeout 20 --stop 2>/dev/null || true
ncs --with-package-reload --cd $LABDIR $CONF
