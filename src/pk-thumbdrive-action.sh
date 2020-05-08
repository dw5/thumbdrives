#!/bin/sh
ACTION=$1
BACKING_FILE=$2
CONFIGFS=/sys/kernel/config/usb_gadget
GADGET=$CONFIGFS/thumbdrives

remove_gadget () {
	local gadget=$1

	# Disable the gadget
	echo "" > "$gadget"/UDC

	# Remove the functions from the config
	for function in "$gadget"/configs/*/*.*
	do
		rm "$function"
	done

	# Remove the language data from the config
	for lang in "$gadget"/configs/*/strings/*
	do
		rmdir "$lang"
	done

	# Remove the configurations
	for config in "$gadget"/configs/*/
	do
		rmdir "$config"
	done

	# Remove the defined functions
	for function in "$gadget"/functions/*/
	do
		rmdir "$function"
	done

	# Remove the defined language data
	for lang in "$gadget"/strings/*
	do
		rmdir "$lang"
	done

	# Remove the gadget
	rmdir "$gadget"
}

disable_existing_gadgets () {
	for gadget in "$CONFIGFS"/*/UDC
	do
		echo "" > "$gadget"
	done
}

create_gadget () {
	local backing="$1"
	local devtype="$2"

	mkdir $GADGET
	echo "0x1209" > $GADGET/idVendor # Generic
	echo "0x4202" > $GADGET/idProduct # Random id

	# English locale
	LOCALE=$GADGET/strings/0x409
	mkdir $LOCALE || echo "Could not create $LOCALE"
	echo "Phone" > $LOCALE/manufacturer
	echo "BLEH" > $LOCALE/product
	echo "Thumbdrives" > $LOCALE/serialnumber

	# Mass storage function
	FUNCTION=$GADGET/functions/mass_storage.0
	LUN=$FUNCTION/lun.0
	mkdir $FUNCTION || echo "Could not create $FUNCTION"
	mkdir $LUN || echo "Could not create $LUN"

	# Configuration instance
	CONFIG=$GADGET/configs/c.1
	LOCALE=$CONFIG/strings/0x409
	mkdir $CONFIG || echo "Coud not create $CONFIG"
	mkdir $LOCALE || echo "Coud not create $LOCALE"
	echo "Thumbdrive" > $LOCALE/configuration

	# Link mass storage gadget to backing file
	echo $backing > $LUN/file
	echo $devtype > $LUN/cdrom

	# Mass storage hardware name
	echo "Thumbdrives" > $LUN/inquiry_string

	# Add mass storage to the configuration
	ln -s $FUNCTION $CONFIG

	# Link to controller
	echo "$(ls /sys/class/udc)" > $GADGET/UDC || ( echo "Couldn't write to UDC" )
}


if [ "$ACTION" = "mount-mass-storage" ]
then

	[ -d $GADGET ] && remove_gadget $GADGET
	disable_existing_gadgets
	create_gadget "$BACKING_FILE" "0"
fi

if [ "$ACTION" = "mount-iso" ]
then

	[ -d $GADGET ] && remove_gadget $GADGET
	disable_existing_gadgets
	create_gadget "$BACKING_FILE" "1"
fi

if [ "$ACTION" = "umount" ]
then
	[ -d $GADGET ] && remove_gadget $GADGET
fi
