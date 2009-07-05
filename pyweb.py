#!/usr/bin/env python

import gobject, gtk, pango, webkit, re, os, sys

class PyWeb:
    def __init__(self, uri='about:blank'):
        gobject.threads_init()

        self.insert_mode = False
        self.status_format = "%(mode)s [%(keycmd)s] %(uri)s :: %(title)s"
        self.keycmd = ''
        self.title = ''
        self.uri = ''
        self.bindings = Bindings()

        self.window = gtk.Window()
        self.vbox = gtk.VBox()
        self.webview = webkit.WebView()
        self.mainbar = gtk.Label()

        self.mainbar.set_use_markup(True)
        self.mainbar.set_justify(gtk.JUSTIFY_LEFT)
        self.mainbar.set_line_wrap(False)
        self.mainbar.set_selectable(False)
        self.mainbar.set_padding(2,2)
        self.mainbar.set_alignment(0,0)
        self.mainbar.set_ellipsize(pango.ELLIPSIZE_END)
        self.mainbar.set_text("")
 
        self.vbox.pack_start(self.webview, True, True, 0)
        self.vbox.pack_end(self.mainbar, False, False, 0)
        self.window.add(self.vbox)

        self.window.connect('destroy', self._destroy)
        self.window.connect('key-press-event', self._key_press)
        self.webview.connect("load-finished", self._view_load_finished)

        self.webview.open(uri)

        self.mainbar.show()
        self.webview.show()
        self.vbox.show()
        self.window.show()

    def main(self):
        gtk.main()

    def quit(self):
        gtk.main_quit()

    def set_insert_mode(self):
        self.insert_mode = True

    def update_status(self):
        dic = {'mode': 'I' if self.insert_mode else 'C',
                'keycmd': self.keycmd,
                'uri': self.uri,
                'title': self.title}
        self.mainbar.set_text(self.status_format % dic)

    def add_binding(self, binding, callback):
        self.bindings.add(binding, callback)

    def run_keycmd(self, forced=False):
        callback = self.bindings.get_callback(self.keycmd, forced)
        if callback:
            func, args = callback
            func(*args)
            return True

    def _destroy(self, widget):
        self.quit()

    def _view_load_finished(self, view, frame):
        self.title = frame.get_title()
        self.uri = frame.get_uri()
        self.update_status()

    def _key_press(self, widget, event):
        if self.insert_mode and gtk.gdk.keyval_name(event.keyval) != 'Escape':
            self.update_status()
            return False
        if gtk.gdk.keyval_name(event.keyval) == 'Escape':
            if self.insert_mode:
                self.insert_mode = False
            else:
                self.keycmd = ''
            self.update_status()
        elif gtk.gdk.keyval_name(event.keyval) == 'BackSpace':
            self.keycmd = self.keycmd[:-1]
            self.update_status()
        elif gtk.gdk.keyval_name(event.keyval) == 'Return':
            if self.run_keycmd(True):
                self.keycmd = ''
        elif len(event.string) > 0:
            self.keycmd += event.string
            if self.run_keycmd():
                self.keycmd = ''
            self.update_status()
        return True

class Bindings:
    def __init__(self):
        self.bindings = {}
        self.re_bindings = {}

    def add(self, keycmd, callback):
        if '_' in keycmd:
            self.re_bindings[keycmd.replace('_', '(.*)')] = callback
        else:
            self.bindings[keycmd] = callback

    def get_callback(self, keycmd, forced=False):
        if not forced:
            if keycmd in self.bindings:
                return (self.bindings[keycmd], ())
        else:
            for bind in self.re_bindings:
                m = re.match(bind, keycmd)
                if m:
                    return (self.re_bindings[bind], m.groups())

if __name__ == "__main__":
    pyweb = PyWeb()
    confdir = os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.expanduser("~/.config")),'pyweb')
    if os.path.isdir(confdir):
        sys.path.insert(0, confdir)
    try:
        import pywebrc
        pywebrc.init(pyweb)
    except ImportError:
        pass
    pyweb.main()
