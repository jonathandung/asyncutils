__all__ = 'apargs', 'partial', 'Placeholder'
if __import__('sys').version_info >= (3, 14):
    apargs = {'suggest_on_error': True, 'color': __import__('os').getenv('PYTHON_BASIC_REPL') != '1'}
    from _functools import partial, Placeholder # type: ignore[import-not-found]
else: from .compat_313 import apargs, partial, Placeholder