#!/usr/bin/env python

from gettext import gettext as _

import gobject
import gtk
import pango
import webkit

# use GtkStatusbar
# cache: .cache/pyweb/http/holizz.com/p/Depiction + db of mimetypes
class PyWeb:
    def __init__(self):
        gobject.threads_init()

        self.window = gtk.Window()
        self.webview = webkit.WebView()
        self.vbox = gtk.VBox()
        self.vbox.add(self.webview)
        self.window.add(self.vbox)

        self.webview.show()
        self.vbox.show()
        self.window.show()

        self.webview.open('data:text/plain,hi')

    def main(self):
        gtk.main()

if __name__ == "__main__":
    pyweb = PyWeb()
    pyweb.main()
