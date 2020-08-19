# Start NSO instance and stop the previous one if required

echo "Restarting NSO in $LABDIR"
ncs --timeout 20 --stop 2>/dev/null || true
ncs --with-package-reload --cd $LABDIR
