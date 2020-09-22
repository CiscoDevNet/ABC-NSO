# Source ncsrc and prepare NSO running directory:
# - add symlinks to NEDs from <lab>/ned.list
# - copy packages from <lab>/packages/
# - load CDB data from <lab>/cdb/

NCSRC="$NSODIR/ncsrc"
if [ ! -e "$NCSRC" ]; then
	NCSRC="$BASEDIR/ncsrc"
fi
if [ ! -e "$NCSRC" ]; then
	NCSRC=`ls ~/*/ncsrc | sort | tail -n 1`
fi

. $NCSRC
echo "Found NSO in $NCS_DIR"


echo "Running ncs-setup"
ncs-setup --dest $LABDIR

if [ -f "$LAB/ncs.conf" ]; then
	cp -f $LAB/ncs.conf $LABDIR/
fi

if [ -f "$LAB/ned.list" ]; then
	echo "Adding NEDs"
	for ned in `cat $LAB/ned.list`; do
		PKG=`ls -d $NCS_DIR/packages/neds/$ned* | sort | tail -n 1`
		if [ -n "$DEBUG" ]; then echo "  $ned -> $PKG"; fi
		ln -s $PKG $LABDIR/packages/
	done
fi

if [ -d "$LAB/packages" ]; then
	echo "Adding services"
	cp -a $LAB/packages/* $LABDIR/packages/
fi

if [ -d "$LAB/cdb" ]; then
	echo "Adding data"
	cp -a $LAB/cdb/* $LABDIR/ncs-cdb/
fi
