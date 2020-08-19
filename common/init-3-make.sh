# Compile NSO packages if not already
for pkg in `ls -d $LABDIR/packages/*`; do
	FXS=`ls $pkg/load-dir/*.fxs 2>/dev/null || true`
	if [ ! "$FXS" ]; then
		echo "Compiling `basename $pkg`"
		make -C $pkg/src >/dev/null
	fi
done
