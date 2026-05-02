# Examples

Below are some examples of how the asyncutils module can be used, demonstrated right in the tailor-made async-native asyncutils REPL console.

```python
>>> # example 1: Rendezvous
>>> rdv = channels.Rendezvous[int]()
>>> (await asyncio.gather(*map(rdv.put, range(5, 10)), rdv.exchange(10), *map(rdv.exchange, range(1, 5)), *(rdv.get() for _ in range(5))))[-10:]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> task = rdv._loop.create_task(rdv.put(0))
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
>>> from .version import VersionInfo, normalize
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
>>> autogenerate_normalizers()
True
>>> normalize(Decimal('1.2345'))
(1, 23, 45)
>>> normalize(Fraction(1, 3))
(1, 3, 0)
```

The following commands can all enter the console to verify the above, ordered in approximately descending order of preference. They have no known
behavioural differences:

```bash
asyncutils
python -m asyncutils
python asyncutils
python -m asyncutils.__main__
python asyncutils/__main__.py
python -m asyncutils/__main__.py
```
