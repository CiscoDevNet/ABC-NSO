# Configurable variables; empty means do not use.

LABLINK="$HOME/nso-lab"
NSODIR="$HOME/nso"


# Allow per-lab override
if [ -f "$LAB/var.list" ]; then
	. $LAB/var.list
fi
