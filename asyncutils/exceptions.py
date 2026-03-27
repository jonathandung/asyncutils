from sys import stderr, exception, audit
from ._internal.helpers import subscriptable
from ._internal.patch import patch_function_signatures
from ._internal.submodules import exceptions_all as __all__
CRITICAL = SystemExit, SystemError, KeyboardInterrupt
t, a = lambda _: True, lambda _: None
def _unnest_helper(f, g, h, s, /, *, raise_critical=True, keep=Exception, filter_out=(), predicate=t, ack1=a, ack2=a, ack3=a, _a=audit):
    _a('asyncutils.exceptions.unnest'+'_reverse'*isinstance(s, list), s)
    while s:
        if isinstance(group := f(), BaseExceptionGroup): g(group.exceptions)
        elif raise_critical and isinstance(group, CRITICAL): raise Critical(group)
        elif isinstance(group, keep):
            if isinstance(group, filter_out): ack1(group)
            elif not predicate(group): ack2(group)
            elif (y := (yield group)) is not None: h(y)
        else: ack3(group)
def unnest(g, *A, _d=__import__('_collections').deque, _h=_unnest_helper, **k): (s := _d(g.exceptions)).extend(A) if isinstance(g, BaseExceptionGroup) else (s := _d(A)).appendleft(g); return _h(s.popleft, lambda e, g=s.extendleft: g(reversed(e)), s.appendleft, s, **k)
def unnest_reverse(g, *A, _h=_unnest_helper, **k): (g := (s := list(g.exceptions) if isinstance(g, BaseExceptionGroup) else [g]).extend)(A); return _h(s.pop, g, s.append, s, **k)
def potent_derive(*groups, ordered=True, **k):
    n = (P := lambda _, p=(p := k.pop): p(_, None))('notes')
    if not isinstance(g := groups[0], BaseExceptionGroup): *_, t = p('suppress', False), *map(P, ('context', 'cause', 'traceback')); (g := BaseExceptionGroup(p('message'), tuple((unnest if ordered else unnest_reverse)(*groups, **k)))).__suppress_context__, g.__context__, g.__cause__ = _
    if n:
        if isinstance(n, str): g.add_note(n)
        else:
            try: g.__notes__.extend(n)
            except AttributeError: g.__notes__ = list(n)
    return g.with_traceback(t)
def prepare_exception(e, /, *, traceback=None, cause=None, context=None, suppress=False, notes=(), _e=exception):
    if not isinstance(e, BaseException): raise TypeError(f'cannot prepare non-exception: {e!r}')
    if isinstance(notes, str): e.add_note(notes)
    elif (n := getattr(e, '__notes__', None)) is None: e.__notes__ = list(notes)
    else: n.extend(notes)
    if cause is None is e.__context__: e.__context__ = context or _e()
    else: e.__cause__ = cause
    e.__suppress_context__ = suppress; return e.with_traceback(traceback)
def raise_(e, /, *a, traceback=None, cause=None, context=None, suppress=False, notes=(), _a_=audit, _s_=stderr, **k):
    if isinstance(e, type): e = e(*a, **k)
    elif a or k: _s_.write('raise_: no additional arguments were expected\n')
    _a_('asyncutils.exceptions.raise_', e := prepare_exception(e, traceback=traceback, cause=cause, context=context, suppress=suppress, notes=notes)); raise e
patch_function_signatures((unnest, s := 'group, *additional, raise_critical=True, keep={0}, filter_out=(), predicate={0}, ack1={0}, ack2={0}, ack3={0}'), (unnest_reverse, s), (prepare_exception, 'exc, /, *, traceback=None, cause=None, context=None, suppress=False, notes=()'), (raise_, 'exc, /, *args, traceback=None, cause=None, suppress=False, notes=(), **kwds'), (potent_derive, 'group, /, *groups, message={0}, ordered=True, predicate={0}, raise_critical=True, keep={0}, filter_out=(), predicate={0}, ack1={0}, ack2={0}, ack3={0}, notes=None, traceback=None, context=None, cause=None, suppress=False'))
@subscriptable
class _ExceptionWrapper:
    __slots__ = '__exc'
    def __new__(cls, exc):
        if isinstance(exc, CRITICAL): raise exc
        (s := super().__new__(cls)).__exc = exc; return s
    def __getattr__(self, name, /): return getattr(self.__exc, name)
    def __repr__(self): return f'_ExceptionWrapper({self.__exc!r})'
    def __init_subclass__(cls): raise TypeError('cannot subclass _ExceptionWrapper')
exception_occurred, wrap_exc, unwrap_exc = _ExceptionWrapper.__instancecheck__, _ExceptionWrapper.__new__.__get__(_ExceptionWrapper), _ExceptionWrapper._ExceptionWrapper__exc.__get__ # type: ignore[attr-defined]
@subscriptable
class ref:
    __slots__ = '__obj'
    def __new__(cls, obj, r=__import__('_weakref').ref):
        if isinstance(obj, (cls, r)): return obj
        try: return r(obj)
        except TypeError: (_ := object.__new__(cls)).__obj = obj; return _
    def __call__(self): return self.__obj
    def __init_subclass__(cls): raise TypeError('cannot subclass ref')
@subscriptable
class Critical(BaseException):
    def __new__(cls, e=None, /, _m='critical error occurred or user attempted to terminate the program', _e=exception):
        if isinstance(e, cls): return e
        BaseException.__init__(E := BaseException.__new__(cls), _m); E.__context__ = _e() if e is None else e; return E
    @property
    def __suppress_context__(self): return False
    @property
    def exc(self): return self.__cause__ or self.__context__
class StateCorrupted(BaseException):
    def __init__(self, a, d, /): self.adjective, self.details = a, d; super().__init__(f'asyncutils: user tampered with {a} state; {d}')
class Deadlock(BaseException):
    def __init__(self, /, *_, noticer=None): super().__init__(*_); self.noticer = noticer
class IgnoreErrors:
    __slots__ = 'exc'
    def __init__(self, /, *_): self.exc = _ or (Exception,)
    def __enter__(self): return self
    def __exit__(self, t, /, *_): return issubclass(t or object, self.exc)
    async def __aenter__(self): return self
    async def __aexit__(self, *_): return self.__exit__(*_)
    def combined(self, *others): return type(self)(*{*self.exc, *(others if isinstance(others[0], type) else (_.exc for _ in others))})
class VersionError(Exception): ...
for A, B in (('obj', '_refo'), ('normalizer', '_refn'), ('exc', '_refe')):
    def _(self, a=A, b=B):
        if (r := getattr(self, b, None)) is None: raise AttributeError(f"object of type {type(self).__qualname__!r} has no attribute {a!r}")
        if isinstance(r, ref) and (r := r()) is None: raise RuntimeError(f'{a} has been garbage collected')
        return r
    _.__name__, _.__qualname__ = A, f'VersionError.{A}'; setattr(VersionError, A, property(_))
class VersionConversionError(VersionError): ...
class VersionValueError(VersionConversionError, ValueError): ...
@subscriptable
class VersionNormalizerMissing(VersionConversionError, TypeError):
    def __init__(self, o, /, t='attempt to normalize object {0!r} of type {0.__class__.__qualname__!r} failed since a normalizer has not been registered'.format): self._refo = ref(o); super().__init__(t(o))
@subscriptable
class VersionNormalizerTypeError(VersionConversionError, TypeError):
    def __init__(self, /, *a, t='custom normalizer {0!r} for type {1.__class__.__qualname__!r} did not return an iterable of ints as expected when handling {1!r}'.format): self._refn, self._refo = map(ref, a); super().__init__(t(*a))
@subscriptable
class VersionNormalizerFault(VersionConversionError):
    def __init__(self, /, *a, t='custom normalizer {0!r} for type {1.__class__.__qualname__!r} threw {2.__class__.__qualname__} when passed {1!r}'.format): self._refn, self._refo, self._refe = map(ref, a); super().__init__(t(*a))
class VersionCorrupted(VersionError, RuntimeError):
    def __init__(self, o, /, t='instance of %s at %#x was tampered with by the user (parts: %r; should be a tuple of 3 positive integers)'): self._refo = ref(o); super().__init__(t%(type(o).__qualname__, id(o), getattr(o, 'parts', '<not present>')))
    def __getattr__(self, name, /): return getattr(self.obj, name)
class BulkheadError(RuntimeError): ...
class BulkheadFull(BulkheadError): ...
class BulkheadShutDown(BulkheadError): ...
class PoolError(RuntimeError): ...
class PoolFull(PoolError): ...
class PoolShutDown(PoolError): ...
class BusError(Exception): ...
class BusTimeout(BusError, TimeoutError): ...
class BusShutDown(BusError): ...
class BusStatsError(BusError): ...
class BusPublishingError(BusError):
    def __init__(self, /, *_, t='{.name}: severe error in middleware {!r}'.format): self._rb, self._rm = map(ref, _); super().__init__(t(*_))
    @property
    def bus(self): return self._rb()
    @property
    def middleware(self): return self._rm()
class CircuitBreakerError(RuntimeError): ...
class CircuitHalfOpen(CircuitBreakerError): ...
class CircuitOpen(CircuitBreakerError): ...
class EventValueError(ValueError): ...
class FutureCorrupted(RuntimeError): ...
class MaxIterationsError(RuntimeError): ...
class ItemsExhausted(ValueError): ...
class RateLimitExceeded(RuntimeError):
    def __init__(self, f, a, k, c, p, l): self._f, self._a, self._k = f, a, k; super().__init__(f'rate limit of {c} calls in {p} periods exceeded by {l} calls when calling {f!r}')
    async def repeat_call(self): return await self._f(*self._a, **self._k)
class LockForceRequest(BaseException):
    def __init__(self, s, a, l, i, /): self.requester, self.fulfill, self.lock = s, a, l; super().__init__(f'request from {type(s).__qualname__} to release {type(l).__qualname__}', i)
class PasswordQueueError(Exception): ...
class PasswordRetrievalError(PasswordQueueError):
    def __init__(self, from_): self.from_ = from_; super().__init__('failed to retrieve correct password of password-protected queue from closure variable of name %r'%from_)
class GetPasswordRetrievalError(PasswordRetrievalError): ...
class PutPasswordRetrievalError(PasswordRetrievalError): ...
class ForbiddenOperation(PasswordQueueError, TypeError):
    def __init__(self, op, *a): self.op = op = op%a; super().__init__('cannot %s PasswordQueue'%op)
class PasswordError(PasswordQueueError):
    @property
    def wrongpass(self): return self._refp() # type: ignore[attr-defined]
    @property
    def queue(self): return self._refq() # type: ignore[attr-defined]
class WrongPassword(PasswordError, ValueError):
    def __init__(self, *_): self._refq, self._refp = map(ref, _); super().__init__('failure to modify queue because %r received incorrect password: %r'%_)
@subscriptable
class WrongPasswordType(PasswordError, TypeError):
    def __init__(self, *_): self._refp, self._reft, self._refq, self._refc = map(ref, _); super().__init__('password {!r} of wrong type {.__qualname__!r} passed to {!r}; should be {!r}'.format(*_))
    @property
    def wrongtype(self): return self._reft()
    @property
    def correcttype(self): return self._refc()
class PasswordMissing(PasswordQueueError, TypeError): ...
class GetPasswordMissing(PasswordMissing):
    def __init__(self, _='no password provided when trying to get from password-protected queue'): super().__init__(_)
class PutPasswordMissing(PasswordMissing):
    def __init__(self, _='no password provided when trying to put to password-protected queue'): super().__init__(_)
ignore_all = IgnoreErrors(BaseException)
def __getattr__(name, /):
    if name != 'WarningToError': raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
    global WarningToError
    class WarningToError:
        lock = __import__('asyncio.locks', fromlist=('',)).Lock(); __slots__ = '_warn', '_cm'
        def __init__(self, /, *_): self._warn, self._cm = _ or (Warning,), None
        async def __aenter__(self):
            import warnings as _
            async with self.lock: self._cm = c = _.catch_warnings(); c.__enter__(); _.simplefilter('error', self._warn) # type: ignore
        async def __aexit__(self, t, /, *_):
            if (c := self._cm) is None: raise RuntimeError('__aexit__ called without prior __aenter__ call')
            else: c.__exit__(t, *_)
            return issubclass(t or object, Warning)
    return WarningToError
del t, a, s, _, A, B, stderr, _ExceptionWrapper, _unnest_helper, audit, exception