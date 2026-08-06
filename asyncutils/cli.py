__all__ = 'run',
def run(argv=None):
    if isinstance(argv, str): raise TypeError('asyncutils.cli.run: parameter argv must be a non-string iterable')
    import asyncutils as A, asyncutils._internal as I, sys as S; I.parsed.p.parse_args(argv, N := (U := I.unparsed).N)
    if N.command == 'bug': import urllib.parse as p; s = f'https://github.com/jonathandung/asyncutils/issues/new?{p.urlencode({'template': 'bug.yaml', 'pyv': f'Python {S.version} on {S.platform}', 'os': __import__('platform').platform(), 'link': N.src_link, 'cfg': U.z, 'ctx': f'{'\n'.join(map(lambda k, _=__import__('os').environ.get: f'{k}={_(k, '')}', ('AUTILSCFGPATH', 'AUTILSTESTMAXFAIL', 'FORCE_COLOR', 'NO_COLOR', 'PYTHON_BASIC_REPL', 'PYTHONSTARTUP', 'TERM')))}\n*Partly filled by `asyncutils bug`.*'}, quote_via=p.quote)}'; __import__('webbrowser').open(s) if N.open else print(s); S.exit() # cspell: disable-line # ruff: ignore[print]
    I.initialize; S.audit('asyncutils.cli.run') # ruff: ignore[useless-expression]
    try: return A.AsyncUtilsConsole().run(suppress_asyncio_warnings=True, suppress_unawaited_coroutine_warnings=True, always_run_interactive=len(a := S.orig_argv) == 2 and a[0] == S.executable and a[1].endswith(('/bin/autils.exe', '/bin/asyncutils.exe', r'\Scripts\asyncutils.exe', r'\Scripts\autils.exe'))) # ruff: ignore[magic-value-comparison]
    except BaseException as e:
        if not A.pdb: raise
        __import__('_warnings').warn('asyncutils.cli.run: unprecedented exception with no traceback caught; cannot perform autopsy as requested', RuntimeWarning, 2) if (t := e.__traceback__) is None else __import__('pdb').post_mortem(t)
