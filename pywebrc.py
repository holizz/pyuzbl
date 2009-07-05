
def init(pyweb):
    pyweb.add_binding('i', pyweb.set_insert_mode)
    pyweb.add_binding('b', pyweb.webview.go_back)
    pyweb.add_binding('m', pyweb.webview.go_forward)
    pyweb.add_binding('o _', pyweb.open_uri)
    pyweb.add_binding('ZZ', pyweb.quit)
