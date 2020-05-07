import os
import subprocess

def mount(backing_file, cdimage=False):
    action = 'mount-mass-storage'
    if cdimage:
        action = 'mount-iso'

    subprocess.run(['pkexec', 'pk-thumbdrive-action', action, backing_file])

def unmount():
    subprocess.run(['pkexec', 'pk-thumbdrive-action', 'umount'])

def get_mounted():
    gadget = "/sys/kernel/config/usb_gadget/thumbdrives"
    if not os.path.isdir(gadget):
        return None

    with open(gadget + "/UDC") as handle:
        raw = handle.read()

    if raw.strip() == "":
        return None

    with open(gadget+"/functions/mass_storage.0/lun.1/file") as handle:
        raw = handle.read()

    if raw.strip() == "":
        return None

    return raw.strip()
