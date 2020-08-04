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
    main_stack =Gtk.Template.Child()
    header_stack =Gtk.Template.Child()

    unmount = Gtk.Template.Child()

    thumbdrive_list = Gtk.Template.Child()
    iso_list = Gtk.Template.Child()

    frame_thumbdrive = Gtk.Template.Child()
    no_thumbdrive = Gtk.Template.Child()
    frame_iso = Gtk.Template.Child()
    no_iso = Gtk.Template.Child()

    image_name = Gtk.Template.Child()
    image_size = Gtk.Template.Child()
    size_adj = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        datadir = Path(xdg.BaseDirectory.xdg_data_home) / "thumbdrives"
        if not datadir.is_dir():
            datadir.mkdir()

        downloads = Path("~/Downloads").expanduser()

        for img in datadir.glob('*.img'):
            self.add_img(img)
        for iso in datadir.glob('*.iso'):
            self.add_iso(iso)

        if downloads.is_dir():
            for iso in downloads.glob('*.iso'):
                self.add_iso(iso)
            for img in downloads.glob('*.img'):
                self.add_img(img)

        self.update_mounted()

        self.thumbdrive_list.show_all()
        self.iso_list.show_all()
        self.update_visibility()

        self.datadir = datadir

    def add_img(self, path):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        icon = Gtk.Image()
        icon.set_size_request(16, 16)
        label = Gtk.Label(path.name.replace(".img", ""), xalign=0)
        label.set_margin_top(8)
        label.set_margin_bottom(8)
        box.pack_start(icon, False, False, False)
        box.pack_start(label, True, True, False)
        box.filename = str(path)
        self.thumbdrive_list.insert(box, -1)

    def add_iso(self, path):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        icon = Gtk.Image()
        icon.set_size_request(16, 16)
        label = Gtk.Label(path.name.replace(".iso", ""), xalign=0)
        label.set_margin_top(8)
        label.set_margin_bottom(8)
        box.pack_start(icon, False, False, False)
        box.pack_start(label, True, True, False)
        box.filename = str(path)
        self.iso_list.insert(box, -1)

    def update_visibility(self):
        has_thumbdrives = len(list(self.thumbdrive_list)) > 0
        has_iso = len(list(self.iso_list)) > 0

        if has_thumbdrives:
            self.no_thumbdrive.hide()
            self.frame_thumbdrive.show()
        else:
            self.no_thumbdrive.show()
            self.frame_thumbdrive.hide()

        if has_iso:
            self.no_iso.hide()
            self.frame_iso.show()
        else:
            self.no_iso.show()
            self.frame_iso.hide()


    def update_mounted(self):
        filename = vdisk.get_mounted()
        if filename is None:
            self.unmount.set_sensitive(False)
            self.headerbar.set_subtitle("No drive mounted")
        else:
            self.unmount.set_sensitive(True)
            self.headerbar.set_subtitle("Loaded " + os.path.basename(filename))

        for row_wrapper in self.thumbdrive_list:
            box = row_wrapper.get_child()
            icon = None
            for widget in box:
                if isinstance(widget, Gtk.Image):
                    icon = widget
            if box.filename == filename:
                icon.set_from_icon_name('object-select-symbolic', Gtk.IconSize.BUTTON)
            else:
                icon.clear()

        for row_wrapper in self.iso_list:
            box = row_wrapper.get_child()
            icon = None
            for widget in box:
                if isinstance(widget, Gtk.Image):
                    icon = widget
            if box.filename == filename:
                icon.set_from_icon_name('object-select-symbolic', Gtk.IconSize.BUTTON)
            else:
                icon.clear()


    @Gtk.Template.Callback()
    def on_image_row_activated(self, listbox, row):
        box = row.get_child()
        filename = box.filename

        if ".iso" in filename:
            vdisk.mount(filename, cdimage=True)
        else:
            vdisk.mount(filename)

        listbox.unselect_all()

        self.update_mounted()

    @Gtk.Template.Callback()
    def on_unmount_clicked(self, button):
        vdisk.unmount()
        self.update_mounted()

    @Gtk.Template.Callback()
    def on_back_clicked(self, button):
        self.main_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)
        self.main_stack.set_visible_child_name('home')
        self.header_stack.set_visible_child_name('home')

    @Gtk.Template.Callback()
    def on_add_thumbdrive_clicked(self, button):
        self.main_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.main_stack.set_visible_child_name('add_thumbdrive')
        self.header_stack.set_visible_child_name('back')

    @Gtk.Template.Callback()
    def on_create_clicked(self, button):
        name = self.image_name.get_text()
        size = self.size_adj.get_value()

        filename = os.path.join(self.datadir, name + ".img")

        with open(filename, 'ab') as handle:
            handle.truncate(size * 1024 * 1024)
        self.add_img(filename)
        self.thumbdrive_list.show_all()
        self.update_visibility()
        self.main_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)
        self.main_stack.set_visible_child_name('home')
        self.header_stack.set_visible_child_name('home')
