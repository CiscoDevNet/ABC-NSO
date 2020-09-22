# Configurable variables; empty means do not use.

echo "Setting up environment"
LABLINK="$HOME/run"
NSODIR="$HOME/nso"
ADDSIMDEVS=true


# Allow per-lab override
if [ -f "$LAB/var.list" ]; then
	if [ -n "$DEBUG" ]; then cat $LAB/var.list; fi
	. $LAB/var.list
fi
