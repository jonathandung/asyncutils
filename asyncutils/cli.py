# ruff: file-ignore[compare-to-empty-string, magic-value-comparison, print, read-whole-file]
import sys as S
__all__ = 'bug', 'run'
def _(d, /):
    if len(d) < 0x400: return d
    import urllib.request as l
    with l.urlopen(l.Request('https://paste.rs', d), timeout=6) as r:
        if (c := r.status) == 201: return r.read()
        raise RuntimeError('asyncutils.cli.bug: content truncated; erroring since logs or traceback should not be this big' if c == 206 else f'asyncutils.cli.bug: could not upload to paste.rs due to {r.reason}; status: {c}')
def bug(args, paste=_, j=lambda p, y=S.stdin.buffer.read: print(end=p) or y()): # ruff: ignore[complex-structure, too-many-branches, too-many-statements]
    import asyncutils as A, importlib.metadata as m, urllib.parse as p; h, e, i, t, u, l, d, g, z, o, w = __import__('os').environ.get, args.ensure_filled, args.interactive, args.title, args.src_url, args.verbose-args.quiet, args.pastebin, args.log_path, args.traceback_path, args.open, S.stderr.write
    try: v = m.version('py-asyncutils')
    except m.PackageNotFoundError:
        if l > -1:
            w('py-asyncutils package not installed\n')
            if l: w("Falling back to filling package version field with 'Not installed'\n")
        v = 'Not installed'
    if i:
        f = True
        if not t:
            f, t = False, input('Bug report title: ' if l == 1 else 'Title: ' if l == 0 else 'title=')
            if e and not t: raise ValueError('asyncutils.cli.bug: title is missing')
        if not u:
            f, u = False, input('Paste the source file permalink: ' if l == 1 else 'Source URL: ' if l == 0 else 'link=')
            if e and not u: raise ValueError('asyncutils.cli.bug: source URL is missing')
        if g == '': f, g = False, j('Paste the debug logs (not the file path): ' if l == 1 else 'Logs (debug level): ' if l == 0 else 'logs=')
        if z == '':
            f, z = False, j('Paste the traceback (not the file path): ' if l == 1 else 'Traceback: ' if l == 0 else 'tb=')
            if z:
                if not z.startswith(b'Traceback (most recent call last):\n'): raise ValueError('asyncutils.cli.bug: malformed traceback')
            elif e: raise ValueError('asyncutils.cli.bug: traceback is missing')
        if not g: g = b''
        if not z: z = b''
        if f and l == 1: print('All fields have already been filled by command-line arguments despite --interactive.')
    else:
        if e:
            a = (r := []).append
            if not t: a(ValueError('title is missing'))
            if not u: a(ValueError('source URL is missing'))
            if g == '': a(ValueError('log path not passed'))
            if z == '': a(ValueError('traceback path not passed'))
            if r: raise ExceptionGroup('asyncutils.cli.bug: one or more required fields are empty and --ensure-filled was passed', r)
        if g:
            with open(g, 'rb') as f: g = f.read()
        else: g = b''
        if z:
            with open(z, 'rb') as f: z = f.read()
        else: z = b''
    if not t.startswith(b := 'Bug: '): t = b+t
    if u and not ((r := p.urlsplit(u)).scheme and r.netloc): raise ValueError(f'asyncutils.cli.bug: invalid source link {u!r}')
    S.audit('asyncutils.cli.bug', s := f'https://github.com/jonathandung/asyncutils/issues/new?{p.urlencode({'template': 'bug.yaml', 'title': t, 'auv': A.__version__.representation, 'pkv': v, 'pyv': f'Python {S.version} on {S.platform}', 'os': __import__('platform').platform(), 'link': u, 'logs': paste(g) if d else g, 'tb': paste(z) if d else z, 'cfg': A._internal.unparsed.z, 'env': '' if args.no_prefill_env else '\n'.join(f'{k}={h(k, '')}' for k in ('AUTILSCFGPATH', 'AUTILSTESTMAXFAIL', 'FORCE_COLOR', 'NO_COLOR', 'PYTHON_BASIC_REPL', 'PYTHONSTARTUP', 'TERM'))}, quote_via=p.quote)}') # cspell: disable-line
    if o is NotImplemented: print(s); return 0
    import webbrowser as c; c.register_standard_browsers() # ty: ignore[unresolved-attribute]
    if l == 1: print(f'Attempting to open link in {(x := 'default browser' if o is None else o)}')
    if (c.get(o) if o is None or o in c._browsers else c.BackgroundBrowser(o)).open(s): return 0 # ty: ignore[unresolved-attribute]
    if args.print_on_fail:
        if l > -1: w(f'Failed to open link in {x}; printing link to console instead\n' if l else 'Could not open issue; link below\n') # ty: ignore[possibly-unresolved-reference]
        print(s)
    return 1
def run(argv=None):
    if isinstance(argv, str): raise TypeError('asyncutils.cli.run: argv must be a non-string iterable')
    import asyncutils as A, asyncutils._internal as I; I.parsed.p.parse_args(argv, n := I.unparsed.N)
    if n.pop('command') == 'bug': return bug(n)
    del n; I.initialize; S.audit('asyncutils.cli.run'); p = not A.pdb # ruff: ignore[useless-expression]
    try: return A.AsyncUtilsConsole().run(suppress_asyncio_warnings=p, suppress_unawaited_coroutine_warnings=p, always_run_interactive=len(a := S.orig_argv) == 2 and a[0] == S.executable and a[1].endswith(('/bin/autils.exe', '/bin/asyncutils.exe', r'\Scripts\asyncutils.exe', r'\Scripts\autils.exe')))
    except BaseException as e:
        if p: raise
        t = e.__traceback__
    __import__('_warnings').warn('asyncutils.cli.run: unprecedented exception with no traceback caught; cannot perform autopsy as requested', RuntimeWarning, 2) if t is None else __import__('pdb').post_mortem(t)
del _
