
import gtk, os, sys, subprocess

def init(pyweb, pwlib):
    confdir = os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.expanduser("~/.config")),'pyweb')
    datadir = os.path.join(os.environ.get('XDG_DATA_HOME', os.path.expanduser("~/.local/share")),'pyweb')

    # Events

    def history(webview, frame):
        with open(os.path.join(datadir, 'history'), 'a+') as f:
            f.write(frame.get_uri()+'\n')
    pyweb.webview.connect('load-finished', history)

    #TODO: download
    #TODO: cookies

    # Bindings

    def bind(keycmd, func):
        regexp = False
        if '_' in keycmd:
            keycmd = keycmd.replace('_', '(.*)')
            regexp = True
        pyweb.add_binding(keycmd, func, regexp)
    def bind_u(keycmd, uri):
        bind(keycmd, lambda *u: pyweb.webview.open(uri % u))

    # Navigation

    bind('i', pyweb.set_insert_mode)
    bind('b', pyweb.webview.go_back)
    bind('m', pyweb.webview.go_forward)
    bind('ZZ', pyweb.quit)

#TODO:
#bind j = scroll_vert 20
#bind k = scroll_vert -20
#bind h = scroll_horz -20
#bind l = scroll_horz 20
#bind << = scroll_begin
#bind >> = scroll_end

    bind('s', pyweb.webview.stop_loading)
    bind('r', pyweb.webview.reload)
    bind('R', pyweb.webview.reload_bypass_cache)
    bind('+', pyweb.webview.zoom_in)
    bind('-', pyweb.webview.zoom_out)
    bind('0', lambda: pyweb.webview.set_zoom_level(1))

    bind('t', pyweb.toggle_status)

#TODO:
#bind /* = search %s
#bind ?* = search_reverse %s
#bind n = search
#bind N = search_reverse

    def clip_get():
        return gtk.clipboard_get().wait_for_text()
    def clip_set(s):
        gtk.clipboard_get().set_text(s)

    bind('yy', lambda: clip_set(pyweb.uri))
    bind('p', lambda: pyweb.webview.open(clip_get()))

    bind('Bm', lambda: open(os.path.expanduser('~/bookmarks'),'a+').write(pyweb.uri+'\n'))

    # URIs

    bind('cc', lambda: subprocess.Popen(sys.argv[0]))
    bind('c _', lambda u: subprocess.Popen([sys.argv[0],u]))

    bind('o _', pyweb.webview.open)
    def edit_uri():
        pyweb.keycmd = 'o %s' % pyweb.uri
        raise pwlib['KeycmdResetInhibitor']
    bind('O', edit_uri)

    bind_u('gg _', 'http://www.google.com/search?q=%s')
    bind_u('gl _', 'http://www.google.com/search?btnI=&q=%s')
    bind_u('we _', 'https://secure.wikimedia.org/wikipedia/en/wiki/Special:Search?search=%s')
    bind_u('wj _', 'https://secure.wikimedia.org/wikipedia/ja/wiki/Special:Search?search=%s')
    # Two regexps? uzbl can't do that!
    bind_u('w _ _', 'https://secure.wikimedia.org/wikipedia/%s/wiki/Special:Search?search=%s')
    bind_u('gh _', 'http://github.com/%s')
    bind_u('ghh _', 'http://github.com/holizz/%s')
    bind_u('gp _', 'https://thepiratebay.org/search/%s/0/99/0')
    bind_u('gt _', 'http://search.twitter.com/search?q=%s')

#TODO:
#bind :noscript = set disable_scripts = 1
#bind :script = set disable_scripts = 0
#bind :reload = sh 'cat $1 > "$4"' # reload config
#bind :nocookies = set cookie_handler = sh 'true'
