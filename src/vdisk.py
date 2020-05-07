import subprocess

def mount(backing_file, cdimage=False):
    action = 'mount-mass-storage'
    if cdimage:
        action = 'mount-iso'

    subprocess.run(['pkexec', 'pk-thumbdrive-action', action, backing_file])

def unmount():
    subprocess.run(['pkexec', 'pk-thumbdrive-action', 'umount'])
