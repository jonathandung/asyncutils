# Examples

Below are some examples of how the asyncutils module can be used, demonstrated right in the tailor-made async-native asyncutils REPL console.

```python
>>> load_all() # A function that does the equivalent of the preprocessing done when asyncutils sees the -p/--load-all flag, fetching and executing\
... # all submodules immediately as opposed to finding and importing them on first attribute access; only call if testing the console out\
... # all the code below will still work\
... # example 1: Rendezvous
>>> rdv = channels.Rendezvous[int]() # directly access the submodule object called channels as a global\
... # usually, types that make sense to be generic can be subscripted; see the exact parameters taken in the stub files
>>> (await asyncio.gather(*map(rdv.put, range(5, 10)), rdv.exchange(10), *map(rdv.exchange, range(1, 5)), *(rdv.get() for _ in range(5))))[-10:]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> task = rdv._loop.create_task(rdv.put(0)) # or asyncio.create_task (after importing asyncio, of course)
>>> rdv.state_snapshot()
StateSnapshot(num_getters=0, num_putters=1, num_ops=1, idle=False)
>>> await rdv.get()
0
>>> await rdv.get('default')
'default'
>>> await task
True
>>> task = rdv._loop.create_task(rdv.get())
>>> await rdv.reset()
>>> task.cancelled()
True
>>> # example 2: version
>>> from .version import VersionInfo, normalize # relative imports work as if the root is asyncutils
>>> print(VersionInfo(4, 2).representation)
asyncutils v4.2.0
>>> normalize('1.2.3')
(1, 2, 3)
>>> normalize(19.0203)
(19, 2, 3)
>>> normalize(0x10F0203)
(271, 2, 3)
>>> normalize((1, 3, 5, 7))
(1, 3, 5)
>>> normalize(1.2+3.4j)
(1, 3, 0)
>>> asyncutils.autogenerate_normalizers() # get and call a function defined in the version submodule on the parent module
True
>>> normalize(Decimal('1.2345'))
(1, 23, 45)
>>> normalize(Fraction(1, 3))
(1, 3, 0)
>>> # example 3: symbols
>>> try:
...     DynamicBoundedSemaphore # because the base class of the console implementation uses exec, which requires the namespace to be an exact
...     # instance of dict, accessing most symbols as globals directly will fail
... except NameError as e: print(e)
...
name 'DynamicBoundedSemaphore' is not defined
>>> clear # special command to clear the terminal if supported; not a symbol, but an instance of the primary prompt remains on display
>>> # example 4: accessing documentation
>>> from asyncutils import find_help_url, open_help
>>> find_help_url()
'https://asyncutils.readthedocs.io/en/stable/index.html'
>>> find_help_url('TokenBucket')
'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/buckets/index.html#asyncutils.buckets.TokenBucket'
>>> find_help_url('iters')
'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/iters/index.html#module-asyncutils.iters'
>>> find_help_url(tools)
'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/tools/index.html#module-asyncutils.tools'
>>> find_help_url(signals.wait_for_signal)
'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/signals/index.html#asyncutils.signals.wait_for_signal'
>>> find_help_url('asyncutils.event_loop')
'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/base/index.html#asyncutils.base.event_loop'
>>> find_help_url('__hexversion__')
'https://asyncutils.readthedocs.io/en/stable/top-level.html'
>>> find_help_url(asyncutils.Context)
'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/context/index.html#asyncutils.context.Context'
>>> find_help_url(asyncutils.channels.EventBus.audit_context)
'https://asyncutils.readthedocs.io/en/stable/api/asyncutils/channels/index.html#asyncutils.channels.EventBus.audit_context'
>>> open_help(open_help) # Opens the https://asyncutils.readthedocs.io/en/stable/api/asyncutils/tools/index.html#asyncutils.tools.open_help page\
... # in the system default browser using the standard webbrowser library and returns success
True
```

The following commands can all enter the console to verify the above, ordered in approximately descending order of preference. They have no known
behavioural differences, and the same arguments that the `asyncutils` shell accepts can be appended:

```bash
asyncutils
python -m asyncutils
python asyncutils
python -m asyncutils.__main__
python asyncutils/__main__.py
python -m asyncutils/__main__.py # this is documented to be unsupported, but somehow works
# python asyncutils.__main__ straight up doesn't work
```

If you're in the integrated shell of VS Code, it is recommended that you unset the `PYTHON_BASIC_REPL` environment variable or turn off shell
integration for a better experience in my opinion, since this console does not work well building on the pre-3.12 REPL at all.
