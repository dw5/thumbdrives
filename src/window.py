# window.py
#
# Copyright 2020 Martijn Braam
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

import subprocess
import os

from gi.repository import Gtk
from xdg import XDG_DATA_HOME

import thumbdrives.vdisk as vdisk


@Gtk.Template(resource_path='/nl/brixit/Thumbdrives/window.ui')
class ThumbdrivesWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ThumbdrivesWindow'

    mount = Gtk.Template.Child()
    unmount = Gtk.Template.Child()

    thumbdrive_list = Gtk.Template.Child()
    iso_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        datadir = XDG_DATA_HOME / "thumbdrives"
        if not datadir.is_dir():
            datadir.mkdir()

        for img in datadir.glob('*.img'):
            self.add_img(img)
        for iso in datadir.glob('*.iso'):
            self.add_iso(iso)

    def on_mount_clicked(self, widget, args):
        print("MOUNTING")
        subprocess.run(['truncate', '-s', '16G', '/tmp/test.img'])
        vdisk.mount("/tmp/test.img")

    def on_unmount_clicked(self, widget, args):
        vdisk.unmount()

    def add_img(path):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label = Gtk.Label(path.name.replace(".img", ""))
        box.pack_start(label, True, True, False)
        self.thumbdrive_list.insert(box)

    def add_iso(path):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        label = Gtk.Label(path.name.replace(".iso", ""))
        box.pack_start(label, True, True, False)
        self.iso_list.insert(box)
