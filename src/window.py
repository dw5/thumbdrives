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
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '0.0')
from gi.repository import Gtk, Handy
import xdg.BaseDirectory

import thumbdrives.vdisk as vdisk

Handy.Column()

@Gtk.Template(resource_path='/nl/brixit/Thumbdrives/window.ui')
class ThumbdrivesWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ThumbdrivesWindow'

    headerbar = Gtk.Template.Child()
    thumbdrive_list = Gtk.Template.Child()
    iso_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        datadir = Path(xdg.BaseDirectory.xdg_data_home) / "thumbdrives"
        if not datadir.is_dir():
            datadir.mkdir()

        for img in datadir.glob('*.img'):
            self.add_img(img)
        for iso in datadir.glob('*.iso'):
            self.add_iso(iso)

        self.thumbdrive_list.show_all()
        self.iso_list.show_all()

    def add_img(self, path):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        icon = Gtk.Image()
        label = Gtk.Label(path.name.replace(".img", ""), xalign=0)
        box.pack_start(icon, False, False, False)
        box.pack_start(label, True, True, False)
        box.filename = str(path)
        self.thumbdrive_list.insert(box, -1)

    def add_iso(self, path):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        icon = Gtk.Image()
        label = Gtk.Label(path.name.replace(".iso", ""), xalign=0)
        label.set_margin_top(8)
        label.set_margin_bottom(8)
        box.pack_start(icon, False, False, False)
        box.pack_start(label, True, True, False)
        box.filename = str(path)
        self.iso_list.insert(box, -1)

    def update_mounted():
        filename = vdisk.get_mounted()
        if filename is None:
            self.headerbar.set_subtitle("No drive mounted")
        else:
            self.headerbar.set_subtitle(filename)

    @Gtk.Template.Callback
    def on_image_row_activated(self, listbox, row):
        box = row.get_child()
        filename = box.filename

        if ".iso" in filename:
            vdisk.mount(filename, cdimage=True)
        else:
            vdisk.mount(filename)

        self.update_mounted()
