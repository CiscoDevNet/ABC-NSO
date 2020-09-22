# Compile NSO packages if needed

echo "Checking packages"
for pkg in `ls -d $LABDIR/packages/* 2>/dev/null || true`; do
	if [ -n "$DEBUG" ]; then echo "  $pkg"; fi
	FXS=`ls $pkg/load-dir/*.fxs 2>/dev/null || true`
	if [ ! "$FXS" ]; then
		echo "Compiling `basename $pkg`"
		make -C $pkg/src >/dev/null
	fi
done
