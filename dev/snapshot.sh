#!/bin/bash

set -e

LABDIR=`pwd`
LAB=`mktemp -du ~/nso-save-lab.XXXX`
echo "Saving lab $LABDIR to $LAB"

mkdir -p $LAB
echo "init_common" > $LAB/init.sh

mkdir -p $LAB/cdb
echo "Saving device config"
ncs_load -Fp -p /devices/device > $LAB/cdb/devices.xml
echo "Saving service config"
ncs_load -Fp -p /services > $LAB/cdb/services.xml

if [ -d netsim ]; then
	echo "Creating netsim"
	mkdir -p $LAB/netsim
	DEVS=`ncs-netsim is-alive | cut -f2 -d" "`
	NSDIR=`ncs-netsim whichdir`
	i=0
	for d in $DEVS; do
		NED=`cat $NSDIR/.netsiminfo | grep "abspackagedirs\\[$i\\]" | xargs basename`
		echo "    $i. $d -> $NED"
		echo $NED > $LAB/netsim/$d
		i=$((i+1))
	done
fi

echo "Processing packages"
mkdir -p $LAB/packages
for d in `ls -d ./packages/* || true`; do
	PKG=`basename $d`
	if [ -L $d ]; then
		echo "    Adding $PKG to ned.list"
		echo $PKG >> $LAB/ned.list
	else
		echo "    Copying $PKG"
		cp -a $d $LAB/packages
		if [ -f $LAB/packages/$PKG/src/Makefile ]; then
			echo "    Cleaning $PKG"
			make -s -C $LAB/packages/$PKG/src clean
		fi
	fi
done
ls -d $LAB/packages/* 2>/dev/null || rm -d -v $LAB/packages
