#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

# Set Wayland app_id / program name before initializing GTK
GLib.set_prgname("spotify-popup")
GLib.set_application_name("spotify-popup")

import subprocess
import sys

class SpotifyPopup(Gtk.Window):
    def __init__(self):
        super().__init__(title="Spotify Controller")
        self.set_name("spotify-popup")
        self.set_wmclass("spotify-popup", "spotify-popup")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        
        # Close when clicking outside / losing focus
        self.connect("focus-out-event", self.on_focus_out)
        
        # Layout container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_border_width(14)
        self.add(vbox)
        
        # Song Title
        self.lbl_title = Gtk.Label()
        self.lbl_title.set_markup("<b>Carregando...</b>")
        self.lbl_title.set_ellipsize(3) # Ellipsize at the end
        self.lbl_title.set_max_width_chars(25)
        self.lbl_title.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(self.lbl_title, True, True, 0)
        
        # Artist
        self.lbl_artist = Gtk.Label()
        self.lbl_artist.set_text("")
        self.lbl_artist.set_ellipsize(3)
        self.lbl_artist.set_max_width_chars(25)
        self.lbl_artist.set_halign(Gtk.Align.CENTER)
        self.lbl_artist.get_style_context().add_class("dim-label")
        vbox.pack_start(self.lbl_artist, True, True, 0)
        
        # Action Buttons
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        hbox.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(hbox, True, True, 4)
        
        btn_prev = Gtk.Button(label="⏮")
        btn_prev.connect("clicked", self.on_prev)
        hbox.pack_start(btn_prev, False, False, 0)
        
        self.btn_play = Gtk.Button(label="▶")
        self.btn_play.connect("clicked", self.on_play_pause)
        hbox.pack_start(self.btn_play, False, False, 0)
        
        btn_next = Gtk.Button(label="⏭")
        btn_next.connect("clicked", self.on_next)
        hbox.pack_start(btn_next, False, False, 0)
        
        # Custom CSS styling
        self.apply_css()
        
        # Initial status update
        self.update_info()
        
        # Refresh info every second
        GLib.timeout_add_seconds(1, self.update_info)
        
        self.show_all()
        
    def apply_css(self):
        css = b"""
        window {
            background-color: #1e1e2e;
            border: 1px solid #313244;
            border-radius: 12px;
        }
        label {
            color: #cdd6f4;
            font-family: 'JetBrainsMono Nerd Font', 'Sans';
            font-size: 13px;
        }
        .dim-label {
            color: #a6adc8;
            font-size: 11px;
        }
        button {
            background-color: #313244;
            color: #cdd6f4;
            border-radius: 8px;
            padding: 6px 14px;
            font-family: 'JetBrainsMono Nerd Font', 'Sans';
            font-size: 16px;
            border: none;
            box-shadow: none;
        }
        button:hover {
            background-color: #a55555;
            color: #1e1e2e;
            transition: all 0.2s ease;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
    def on_focus_out(self, widget, event):
        Gtk.main_quit()
        
    def update_info(self):
        try:
            status = subprocess.check_output(["playerctl", "status"], text=True).strip()
            title = subprocess.check_output(["playerctl", "metadata", "title"], text=True).strip()
            artist = subprocess.check_output(["playerctl", "metadata", "artist"], text=True).strip()
        except Exception:
            self.lbl_title.set_markup("<b>Spotify Inativo</b>")
            self.lbl_artist.set_text("")
            self.btn_play.set_label("▶")
            return True
            
        self.lbl_title.set_markup(f"<b>{title}</b>")
        self.lbl_artist.set_text(artist)
        
        if status == "Playing":
            self.btn_play.set_label("⏸")
        else:
            self.btn_play.set_label("▶")
            
        return True
        
    def on_prev(self, button):
        subprocess.run(["playerctl", "previous"])
        self.update_info()
        
    def on_play_pause(self, button):
        subprocess.run(["playerctl", "play-pause"])
        self.update_info()
        
    def on_next(self, button):
        subprocess.run(["playerctl", "next"])
        self.update_info()

if __name__ == "__main__":
    win = SpotifyPopup()
    Gtk.main()
