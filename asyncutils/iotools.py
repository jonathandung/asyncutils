# ruff: file-ignore[global-statement,redefined-loop-name] # ty: ignore[unresolved-attribute]
import errno as E, os as O, sys as S, asyncutils as A
from _functools import partial
from asyncio import Lock, gather
from contextlib import asynccontextmanager
from itertools import starmap
from mmap import mmap
from asyncutils._internal import helpers as H, patch as P
from asyncutils._internal.submodules import iotools_all as __all__
def f(a, b, f=S.audit, _=O.pipe, c=O.close, /):
    def double_ended_pipe(*, pipe_impl=_, x=partial(open, mode=a), y=partial(open, mode=b), f=f):
        r, W, R, w = t = *pipe_impl(), *pipe_impl()
        try: f(f'asyncutils.iotools.double_ended_{'text' if a == 'r' else 'binary'}_pipe', r, w, R, W); yield tuple(map(AsyncReadWriteCouple, map(x, (r, R)), map(y, (w, W))))
        finally:
            for d in t: c(d)
    return A.dualcontextmanager(double_ended_pipe)
s = '*, pipe_impl={}'
double_ended_text_pipe, double_ended_binary_pipe = t = tuple(map(f, ('r', 'rb'), ('w', 'wb')))
P.patch_function_signatures(*((_, s) for _ in t))
@H.subscriptable
class AsyncReadWriteCouple(H.LoopMixinBase):
    __slots__ = '__a', '__x', 'reader', 'writer'; executor = None
    def __init__(self, r, w, /, executor=None, _=H.create_executor, *, find_attr_on_writer_first=False):
        if not r.readable(): raise TypeError(f'asyncutils.iotools.AsyncReadWriteCouple: reader {r!r} is not readable')
        if not w.writable(): raise TypeError(f'asyncutils.iotools.AsyncReadWriteCouple: writer {w!r} is not writable')
        super().__init__(); self.__x, self.reader, self.writer, self.__a = _(t) if executor is None is (executor := (t := type(self)).executor) else executor, r, w, (w, r) if find_attr_on_writer_first else (r, w)
    async def _run(self, *a): return await self.loop.run_in_executor(self.__x, *a)
    def read(self, n=-1, /): return self._run(self.reader.read, n)
    def read1(self, n=-1, /): return self._run(self.reader.read1, n)
    def readall(self): return self._run(r.read if (f := getattr(r := self.reader, 'readall', None)) is None else f)
    async def readinto(self, b, /):
        if (f := getattr(r := self.reader, 'readinto', None)) is not None: return await self._run(f, b)
        if (b := memoryview(b)).readonly: raise TypeError('asyncutils.iotools.AsyncReadWriteCouple: cannot read into a read-only buffer')
        if l := len(d := await self._run(r.read, b.nbytes)): b[:l] = d # cspell:disable-line
        return l
    def readinto1(self, b, /): return self._run(self.reader.readinto1, b)
    def readline(self, l=-1, /): return self._run(self.reader.readline, l)
    def readlines(self, h=-1, /): return self._run(self.reader.readlines, h)
    def write(self, s, /): return self._run(self.writer.write, s)
    def writelines(self, l, /): return self._run(self.writer.writelines, l)
    def __rx(self, e, m, t='tip: delegate to reader or writer as appropriate', /): A.raise_exc(OSError, e, f'asyncutils.iotools.AsyncReadWriteCouple at {id(self):#x}: ambiguous {m} call', notes=t)
    def fileno(self): self.__rx(E.EBADF, 'fileno')
    def isatty(self): self.__rx(E.ENOTSUP, 'isatty')
    readable = writable = lambda _, /: True
    def flush(self): return self._run(self.writer.flush)
    def seekable(self): return False # ruff: ignore[no-self-use]
    def seek(self, *_): self.__rx(E.ESPIPE, 'seek')
    def tell(self): self.__rx(E.ESPIPE, 'tell')
    def truncate(self, s=None, /): return self._run(self.writer.truncate, s)
    async def aclose(self): await gather(*map(self._run, (self.reader.close, self.writer.close))); self.__x.shutdown()
    async def __aenter__(self):
        if self is stdcoup: raise RuntimeError('asyncutils.iotools.AsyncReadWriteCouple: cannot use stdcoup as an async context manager')
        return self
    async def __aexit__(self, *_): await self.aclose()
    @property
    def closed(self): return self.reader.closed and self.writer.closed
    def __getattr__(self, n, /):
        f = (a := []).append
        for _ in self.__a:
            try: return getattr(_, n)
            except AttributeError as e: f(str(e))
        A.raise_exc(AttributeError, f'asyncutils.iotools.AsyncReadWriteCouple: did not find attribute {n!r}', notes=a)
class File(H.LoopMixinBase): # ruff: ignore[too-many-public-methods]
    __slots__ = '__f', '__m', '__n'
    if S.platform != 'win32':
        def madvise(self, option, start=0, length=None, _=H.filter_out): return self.__m.madvise(option, start, *_(length)) # ty: ignore[possibly-missing-attribute]
    def read(self, offset=0, size=-1): return self._run(self.__re, offset, size)
    def write(self, data, offset=0): return self._run(self.__wr, data, offset)
    async def readline(self, offset=0, size=None, include_newline=False): return (await self._run(self.__rl, offset, size, include_newline))[0]
    async def readlines(self, hint=-1): return await A.to_list(await self._run(self.__rs, hint))
    async def flush(self, offset=0, size=None): return await self._run(self.__fl, offset, size)
    def move(self, dest, src, count): return self._run(self.__m.move, dest, src, count)
    async def __aenter__(self): self.__m = m = mmap(self.__n, 0, access=2).__enter__(); self.mgr.add(m)
    async def __aexit__(self, *_): await self.aclose(); self.mgr.discard(self.__m)
    def seek(self, pos, whence=0): return self._run(self.__m.seek, pos, whence)
    def __new__(cls, a, /):
        if (r := (f := cls.open_files.get)((a, 'r+b'))) is None is (r := f((a, 'w+b'))) is (r := f((a, 'x+b'))): (r := super().__new__(cls)).__f, r.__n = a, a.fileno()
        return r
    def __iter__(self): return memoryview(self.__f).__iter__()
    def __aiter__(self): return self.__rs(-1)
    def __del__(self): self.make(self.aclose())
    @property
    def closed(self): return self.__f.closed
    def fileno(self): return self.__n
    def sync(self, _=O.fsync): self.__fl(0, None); _(self.__n)
    async def aclose(self): await gather(*map(self._run, (self.__m.close, self.__f.close)))
    def close(self): self.__m.close(); self.__f.close()
    def read_byte(self): return self.__m.read_byte()
    def write_byte(self, b, /): self.__m.write_byte(b)
    def resize(self, new_size): self.__m.resize(new_size)
    def find(self, sub, start=0, end=-1): return self.__m.find(sub, start, end)
    def rfind(self, sub, start=0, end=-1): return self.__m.rfind(sub, start, end)
    def tell(self): return self.__m.tell()
    def size(self): return self.__m.size()
    def isatty(self): return self.__f.isatty()
    readable = writable = seekable = AsyncReadWriteCouple.readable
    def __fl(self, o, s, _=H.filter_out): self.__f.flush(); self.__m.flush(o, *_(s))
    def __tf(self, d, o): c = (m := self.__m).tell(); m.seek(0, 2); m.resize(max(m.tell(), x := o+len(d))); m.seek(c); return x
    def __re(self, o, s): return self.__m[o:None if s < 0 else o+s]
    def __wr(self, d, o): (m := self.__m)[o:self.__tf(d, o)] = d; m.flush()
    def __rl(self, o, s, i): return (b'', 0) if o >= (l := len(m := self.__m)) else (m[o:(q := p if (e := m.find(b'\n', o, p := (l if s is None else min(o+s, l)))) == -1 else e+i)], q)
    async def __rs(self, h):
        if h < 0: h = float('inf')
        f = self.__rl
        while h > 0: b, n = f(0, None, False); yield b; h -= n
    async def writelines(self, l, /, *, sep=b'', minimize_writes=None):
        f = self.write
        if A.getcontext().MEMORY_MAPPED_IO_MANAGER_DEFAULT_MINIMIZE_WRITES if minimize_writes is None else minimize_writes: return await f(sep.join(await A.to_list(l)))
        g, l = self.__wr, A.iter_to_agen(l)
        if sep:
            async for i in l: await f(i); g(sep, 0)
        else:
            async for i in l: await f(i)
    async def read_str(self, offset=0, size=-1, **k): return (await self.read(offset, size)).decode(**k)
    def write_str(self, text, offset=0, **k): return self.write(text.encode(**k), offset)
    def smart_write(self, data, offset=0, **k): return self.write(data.encode(**k) if isinstance(data, str) else data, offset)
    async def copy_range(self, src_offset, dest_offset, size):
        try: await self.write(await self.read(src_offset, size), dest_offset); return True
        except: return False # ruff: ignore[bare-except]
    def fill(self, pattern, offset=0, count=1): return self.write(pattern*count, offset)
    async def compare(self, o, /, size=-1, offset_self=0, offset_other=0): return (await self.read(offset_self, size)) == (await o.read(offset_other, size))
    async def hamming_dist(self, o, /, size=-1, offset_self=0, offset_other=0, _=int.bit_count): return sum(_(i^j) for i, j in zip(await self.read(offset_self, size), await o.read(offset_other, size), strict=size > 0))
    async def hamming_dist_bytes(self, o, /, size=-1, offset_self=0, offset_other=0): return sum(i != j for i, j in zip(await self.read(offset_self, size), await o.read(offset_other, size), strict=size > 0))
    async def read_until(self, delim, offset=0, maxsize=-1): return (d, offset+len(d)) if (p := (d := await self.read(offset, maxsize)).find(delim)) == -1 else (d[:p+(l := len(delim))], offset+p+l)
    async def insert(self, data, offset): await self.write(data if offset > await self._run(self.size) else data+await self.read(offset), offset)
    async def delete(self, offset, size):
        if size > 0 and offset < (s := await self._run(self.__m.size)):
            if offset < (t := s-size): await self.write(await self.read(offset+size), offset)
            await self._run(self.resize, max(0, t))
    async def replace(self, old, new, offset=0, count=None):
        r, c, o, n, f, g, h = 0, offset, len(old), len(new), partial(self._run, self.find, old), self.delete, self.insert
        if count is None: count = float('inf')
        while r < count:
            if (p := await f(c)) == -1: break
            await g(p, o); await h(new, p); r += 1; c = p+n
        return r
    async def search_lazy(self, pattern, offset=0):
        f = partial(self._run, self.find, pattern)
        async for c in A.acount(offset):
            if (p := await f(c)) == -1: break
            yield p
    async def search_lazy_non_overlapping(self, pattern, offset=0):
        f = partial(self._run, self.find, pattern)
        while True:
            if (offset := await f(offset)) == -1: break
            yield offset
    def search(self, pattern, offset=0, max_results=None): return A.collect(self.search_lazy(pattern, offset), max_results)
    def search_non_overlapping(self, pattern, offset=0, max_results=None): return A.collect(self.search_lazy_non_overlapping(pattern, offset), max_results)
    async def compact(self):
        for i in range(len(c := await self.read())):
            if c[~i]: await self._run(self.resize, c-i); return i
    def __init_subclass__(cls, *, m, r, _=H.simple_wrap): cls.mgr, cls.run, cls.open_files = m, staticmethod(lambda f, /, *a: _(r(f, *a))), {}
class MemoryMappedIOManager(H.LoopMixinBase):
    __slots__ = '__file', '__lock'
    def __init__(self, executor=None, _f=(File,), _=H.create_executor): super().__init__(); self.__file, self.__lock = type('__factory', _f, {}, m=__import__('_weakrefset').WeakSet(), r=partial(self.loop.run_in_executor, _(self, False) if executor is None else executor)), Lock()
    @property
    def open_maps(self): return self.__file.mgr
    def _run(self, f, /, *a): return self.__file.run(f, *a)
    @property
    def currently_open(self): return len(self.open_maps)
    @property
    def open_paths(self): return dict(self.open_files.keys())
    @property
    def open_files(self): return self.__file.open_files
    @open_files.deleter
    def open_files(self): self.open_files.clear()
    @asynccontextmanager
    async def __open(self, s, /, *a):
        if (x := (F := self.open_files).get(a)): yield x; return
        with await (r := self._run)(open, *a) as f:
            if s > 0: await r(f.truncate, s)
            async with self.__file(f) as x:
                F[a] = x
                try: yield x
                finally: F.pop(a, None)
    def open(self, path, init_size=0): return self.__open(init_size, path, 'r+b')
    def create(self, path, init_size=0, *, exclusive=True): return self.__open(init_size, path, 'x+b' if exclusive else 'w+b')
    async def __aenter__(self): return self
    async def __aexit__(self, /, *_):
        async with self.__lock: self.open_maps.clear(); await gather(*(f.close() for f in self.open_files.values())); del self.open_files
    async def copy_file(self, src, dest, *, exclusive=True, flush=False):
        async with self.open(src) as s, self.create(dest, exclusive=exclusive) as d:
            await d.write(await s.read())
            if flush: await d.flush()
    async def checksum(self, path, alg=None, _=partial(__import__('hashlib').new, usedforsecurity=False)):
        async with self.open(path) as f: return await self._run(_, A.getcontext().MEMORY_MAPPED_IO_MANAGER_DEFAULT_CHECKSUM_ALG if alg is None else alg, await f.read()).hexdigest()
    async def approx_memory_usage(self):
        async with self.__lock: return await self._run(self.__mu)
    def __mu(self): return sum(m.size() for m in self.open_maps)
    @asynccontextmanager
    async def prefetch_files(self, *P, init_size=0, _=S.exc_info):
        l = tuple(map(partial(self.open, init_size=init_size), P))
        try: yield await gather(*(c.__aenter__() for c in l)) # ruff: ignore[unnecessary-dunder-call]
        finally: t = _(); await gather(*(c.__aexit__(*t) for c in l))
    @asynccontextmanager
    async def create_sparse_file(self, path, total_size, chunks):
        async with self.create(path, total_size) as f:
            g = f.smart_write
            for o, d in chunks: await g(d, o)
            yield f
    async def _bulk_reader(self, path, offsets):
        a = (r := []).append
        async with self.open(path) as f:
            f = f.read
            if offsets is None: a(await f())
            else:
                for o, s in offsets: a(await f(o, s))
        return path, r
    async def _bulk_writer(self, path, data):
        async with self.open(path) as f: await gather(*starmap(f.write, data))
    async def _checksum_helper(self, alg, path): return path, await self.checksum(path, alg)
    async def _resize_helper(self, path, size):
        async with self.open(path) as f: await self._run(f.resize, size)
    async def _compact_helper(self, path):
        async with self.open(path) as f: await f.compact()
    async def _search_helper(self, p, a, *_):
        async with self.open(p) as f: return p, await (f.search if a else f.search_non_overlapping)(*_)
    async def bulk_read(self, file_offsets): return dict(await gather(*starmap(self._bulk_reader, file_offsets)))
    async def bulk_write(self, file_data): await gather(*starmap(self._bulk_writer, file_data))
    async def bulk_checksum(self, paths, alg=None): return dict(await gather(*map(partial(self._checksum_helper, A.getcontext().MEMORY_MAPPED_IO_MANAGER_DEFAULT_CHECKSUM_ALG if alg is None else alg), paths)))
    async def bulk_copy(self, pairs): await gather(*starmap(self.copy_file, pairs))
    async def bulk_resize(self, sizes): await gather(*starmap(self._resize_helper, sizes))
    async def compact_files(self, paths): await gather(*map(self._compact_helper, paths))
    async def find_in_files(self, pattern, paths, max_per_file=None, *, allow_overlapping=False):
        f = self._search_helper
        return {k: v for k, v in await gather(*(f(p, allow_overlapping, pattern, o, max_per_file) for p, o in paths)) if v}
    P.patch_method_signatures((__init__, 'executor=None'), (prefetch_files, '*paths, init_size=0'), (__open, 'init_size, path, mode, /'))
def __getattr__(n, /, a=frozenset(('ainput', 'stdcoup')), g=globals()):
    if n not in a: raise AttributeError(f'module {__name__!r} has no attribute {n!r}')
    global ainput, stdcoup; stdcoup = AsyncReadWriteCouple(S.stdin, S.stdout) # ty: ignore[unresolved-global]
    async def ainput(prompt='', assert_tty=False):
        if prompt: await stdcoup.write(prompt); await stdcoup.flush()
        if assert_tty and not stdcoup.reader.isatty(): raise OSError(E.ENOTTY, 'asyncutils.iotools.ainput: standard input is not a TTY')
        if (d := await stdcoup.readline()).endswith('\n'): return d[:-1]
        raise EOFError
    return g[n]
del f, H, P, File, O, t, s
