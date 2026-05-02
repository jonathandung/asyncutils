from asyncutils import LoopContextMixin, collect, getcontext, iter_to_agen, sync_await
from asyncutils._internal import helpers as H, patch as P
from asyncutils._internal.submodules import io_all as __all__
import os as O, sys as S
from _functools import partial # type: ignore[import-not-found]
from asyncio import Lock, gather
from contextlib import asynccontextmanager
from itertools import count, starmap
from mmap import mmap
def f(a, b, f=S.audit, _=O.pipe, /):
    def double_ended_pipe(*, pipe_impl=_, x=partial(open, mode=a), y=partial(open, mode=b), _=f): r, W, R, w = *pipe_impl(), *pipe_impl(); _(f'asyncutils.io.double_ended_{"text" if a == "r" else "binary"}_pipe', r, w, R, W); return tuple(map(AsyncReadWriteCouple, map(x, (r, R)), map(y, (w, W))))
    return double_ended_pipe
_, s = lambda s=None, /, **d: {k: v for k, v in d.items() if v is not s}, '*, pipe_impl={}'
double_ended_text_pipe, double_ended_binary_pipe = t = tuple(map(f, ('r', 'rb'), ('w', 'wb')))
P.patch_function_signatures(*((_, s) for _ in t))
@H.subscriptable
class AsyncReadWriteCouple(LoopContextMixin):
    __slots__ = 'executor', 'reader', 'writer'
    def __init__(self, r, w, /, executor=None):
        super().__init__()
        if executor is None: self._init_executor()
        else: self.executor = executor
        self.reader, self.writer = r, w
    async def _run(self, f, *a): return await self.loop.run_in_executor(self.executor, f, *a)
    def read(self, n=-1, /): return self._run(self.reader.read, n)
    def readline(self, limit=-1, /): return self._run(self.reader.readline, limit)
    def readlines(self, hint=-1, /): return self._run(self.reader.readlines, hint)
    def write(self, s, /): return self._run(self.writer.write, s)
    def writelines(self, lines, /): return self._run(self.writer.writelines, lines)
    def fileno(self): raise OSError('cannot determine fileno of read-write couple')
    def isatty(self): return self.reader.isatty() or self.writer.isatty()
    def readable(self): return self.reader.readable()
    def writable(self): return self.writer.writable()
    def flush(self): return self._run(self.writer.flush)
    def seekable(self): return self.reader.seekable() and self.writer.seekable()
    def seek(self, offset, whence=0, /): raise OSError('cannot use seek on read-write couple') # noqa: ARG002
    def tell(self): raise OSError('cannot use tell on read-write couple')
    def truncate(self, size=None, /): return self._run(self.writer.truncate, size)
    async def aclose(self): await gather(*map(self._run, (self.reader.close, self.writer.close))); self.executor.shutdown()
    __cleanup__, _init_executor = aclose, H.create_executor
    @property
    def closed(self): return self.reader.closed and self.writer.closed
    def __getattr__(self, n, /):
        try: return getattr(self.reader, n)
        except AttributeError as a:
            try: return getattr(self.writer, n)
            except AttributeError as b: raise ExceptionGroup(f'read-write couple has no attribute {n!r}', (a, b)) from None
class File(LoopContextMixin):
    __slots__ = '_f', '_fn', '_mmap'
    if S.platform != 'win32':
        def madvise(self, option, start=0, length=None, _=H.filter_out): return self.mmap.madvise(option, start, *_(length))
    def read(self, offset=0, size=-1): return self.run(self._read, offset, size)
    def write(self, data, offset=0): return self.run(self._write, data, offset)
    async def readline(self, offset=0, size=None, incl_newline=False): return (await self.run(self._readline, offset, size, incl_newline))[0]
    async def readlines(self, hint=-1): return list(await self.run(self._readlines, hint))
    async def flush(self, offset=0, size=None, /): return await self.run(self._flush, offset, size)
    def move(self, dest, src, count): return self.run(self._mmap.move, dest, src, count)
    async def __setup__(self): self._mmap = m = mmap(self._fn, 0, access=2).__enter__(); self.mgr.add(m)
    async def __cleanup__(self): await self.aclose(); self.mgr.discard(self._mmap)
    def seek(self, pos, whence=0): return self.run(self._mmap.seek, pos, whence)
    def __new__(cls, file, /):
        if (r := (f := cls.open_files.get)((file, 'r+b'))) is None is (r := f((file, 'w+b'))) is (r := f((file, 'x+b'))): (r := super().__new__(cls))._f, r._fn = file, file.fileno()
        return r
    def __iter__(self): return self._f.__iter__()
    def __aiter__(self): return iter_to_agen(self._f)
    def __del__(self): self.make(self.aclose())
    @property
    def closed(self): return self._f.closed
    def fileno(self): return self._fn
    def sync(self, _=O.fsync): self._flush(0, None); _(self._fn)
    async def aclose(self): await gather(*map(self.run, (self._mmap.close, self._f.close)))
    def close(self): self._mmap.close(); self._f.close()
    def read_byte(self): return self._mmap.read_byte()
    def write_byte(self, b, /): self._mmap.write_byte(b)
    def resize(self, newsize): self._mmap.resize(newsize)
    def find(self, sub, start=None, end=None, _=_): return self._mmap.find(sub, **_(start=start, end=end))
    def rfind(self, sub, start=None, end=None, _=_): return self._mmap.rfind(sub, **_(start=start, end=end))
    def tell(self): return self._mmap.tell()
    def size(self): return self._mmap.size()
    def isatty(self): return self._f.isatty()
    readable = writable = seekable = lambda _, /: True
    def _flush(self, offset, size, _=H.filter_out): self._f.flush(); self._mmap.flush(offset, *_(size))
    def _trunc_from(self, data, offset): c = (m := self._mmap).tell(); m.seek(0, 2); m.resize(max(m.tell(), x := offset+len(data))); m.seek(c); return x
    def _read(self, offset, size): return self._mmap[offset:None if size < 0 else offset+size]
    def _write(self, data, offset): (m := self._mmap)[offset:self._trunc_from(data, offset)] = data; m.flush()
    def _readline(self, offset, size, incl_newline): return (b'', 0) if offset >= (l := len(m := self._mmap)) else (m[offset:(q := p if (e := m.find(b'\n', offset, p := (l if size is None else min(offset+size, l)))) == -1 else e+incl_newline)], q)
    def _readlines(self, hint, /):
        if hint < 0: yield from map(bytes, self._mmap); return
        f = self._readline
        while hint > 0: b, n = f(0, None, False); yield b; hint -= n
    async def writelines(self, lines, /, *, sep=b''):
        f = self.write
        for l in lines: await f(l+sep)
    async def read_str(self, offset=0, size=-1, encoding='utf-8', errors='strict'): return (await self.read(offset, size)).decode(encoding, errors)
    def write_str(self, text, offset=0, encoding='utf-8', errors='strict'): return self.write(text.encode(encoding, errors), offset)
    def smart_write(self, data, offset=0, encoding='utf-8', errors='strict'): return self.write(data.encode(encoding, errors) if isinstance(data, str) else data, offset)
    async def copy_range(self, src_offset, dest_offset, size):
        try: await self.write(await self.read(src_offset, size), dest_offset); return True
        except: return False # noqa: E722
    def fill(self, pattern, offset=0, count=1): return self.write(pattern*count, offset)
    async def compare(self, other, /, size=-1, offset_self=0, offset_other=0): return (await self.read(offset_self, size)) == (await other.read(offset_other, size))
    async def hamming_dist(self, other, /, size=-1, offset_self=0, offset_other=0): return sum(x.bit_count() for x in map(int.__xor__, await self.read(offset_self, size), await other.read(offset_other, size), strict=size > 0))
    async def read_until(self, delim, offset=0, maxsize=-1): return (d, offset+len(d)) if (p := (d := await self.read(offset, maxsize)).find(delim)) == -1 else (d[:p+(l := len(delim))], offset+p+l)
    async def insert(self, data, offset): await self.write(data if offset > await self.run(self.size) else data+await self.read(offset), offset)
    async def delete(self, offset, size):
        if size <= 0 or offset >= (s := await self.run(self._mmap.size)): return
        if (t := offset+size) < s: await self.write(await self.read(t), offset)
        await self.run(self.resize, max(0, s-size))
    async def replace(self, old, new, offset=0, count=None):
        r, c, o, n, f, g, h, b = 0, offset, len(old), len(new), partial(self.run, self.find, old), self.delete, self.insert, count is None
        while b or r < count:
            if (p := await f(c)) == -1: break
            await g(p, o); await h(new, p); r += 1; c = p+n
        return r
    async def search_lazy(self, pattern, offset=0):
        f = partial(self.run, self.find, pattern)
        for c in count(offset):
            if (p := await f(c)) == -1: break
            yield p
    async def search_lazy_nonoverlapping(self, pattern, offset=0):
        f = partial(self.run, self.find, pattern)
        while True:
            if (offset := await f(offset)) == -1: break
            yield offset
    def search(self, pattern, offset=0, max_results=None): return collect(self.search_lazy(pattern, offset), max_results)
    def search_nonoverlapping(self, pattern, offset=0, max_results=None): return collect(self.search_lazy_nonoverlapping(pattern, offset), max_results)
    async def compact(self):
        for i in range(len(c := await self.read())-1, -1, -1):
            if c[i]: await self.run(self.resize, i+1); break
    def __init_subclass__(cls, *, m, r):
        @staticmethod
        async def run(f, /, *a, r=r): return await r(f, *a)
        cls.mgr, cls.run, cls.open_files = m, run, {}
class MemoryMappedIOManager(LoopContextMixin):
    __slots__ = '_factory', '_lock'
    def __init__(self, executor=None, _f=(File,), _=H.create_executor): super().__init__(); self._factory, self._lock = type('_factory', _f, {}, m=__import__('_weakrefset').WeakSet(), r=partial(self.loop.run_in_executor, _(self, False) if executor is None else executor)), Lock()
    @property
    def open_mmaps(self): return self._factory.mgr
    def _run(self, f, /, *a): return self._factory.run(f, *a)
    @property
    def currently_open(self): return len(self.open_mmaps)
    @property
    def open_paths(self): return dict(self.open_files.keys())
    @property
    def open_files(self): return self._factory.open_files
    @open_files.deleter
    def open_files(self): self.open_files.clear()
    @asynccontextmanager
    async def _open(self, s, /, *k):
        if (x := (F := self.open_files).get(k)): yield x; return
        try:
            with await (r := self._run)(open, *k) as f:
                if s > 0: await r(f.truncate, s)
                async with self._factory(f) as x: F[k] = x; yield x
        finally: F.pop(k, None)
    def open(self, path, init_size=0): return self._open(init_size, path, 'r+b')
    def create(self, path, init_size=0, *, exclusive=True): return self._open(init_size, path, 'x+b' if exclusive else 'w+b')
    async def __cleanup__(self):
        async with self._lock: self.open_mmaps.clear(); await gather(*(f.close() for f in self.open_files.values())); del self.open_files
    def __del__(self): sync_await(self.__cleanup__(), loop=(l := self.loop)); l.stop(); l.close()
    async def copy_file(self, srcp, destp, *, flush=False):
        async with self.open(srcp) as src, self.create(destp) as dest:
            await dest.write(await src.read())
            if flush: await dest.flush()
    async def checksum(self, path, alg=None):
        async with self.open(path) as f: return __import__('hashlib').new(getcontext().MEMORY_MAPPED_IO_MANAGER_DEFAULT_CHECKSUM_ALG if alg is None else alg, await f.read()).hexdigest()
    async def approx_memory_usage(self):
        async with self._lock: return await self._run(self._memusage_helper)
    def _memusage_helper(self): return sum(m.size() for m in self.open_mmaps)
    @asynccontextmanager
    async def prefetch_files(self, *P, init_size=0, _=S.exc_info):
        try: l = tuple(map(partial(self.open, init_size=init_size), P)); yield await gather(*(c.__aenter__() for c in l))
        finally: t = _(); await gather(*(c.__aexit__(*t) for c in l))
    @asynccontextmanager
    async def create_sparsef(self, path, total_size, chunks):
        async with self.create(path, total_size) as f:
            g = f.smart_write
            for o, d in chunks.items(): await g(d, o)
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
    async def _bulk_creator(self, path, size, chunks, exclusive):
        async with self.create(path, size, exclusive=exclusive) as f:
            f = f.smart_write
            for o, d in chunks.items(): await f(d, o)
    async def _checksum_helper(self, alg, path): return path, await self.checksum(path, alg)
    async def _resize_helper(self, path, size):
        async with self.open(path) as f: await self._run(f.resize, size)
    async def _compact_helper(self, path):
        async with self.open(path) as f: await f.compact()
    async def bulk_read(self, file_offsets): return dict(await gather(*starmap(self._bulk_reader, file_offsets.items())))
    async def bulk_write(self, file_data): await gather(*starmap(self._bulk_writer, file_data.items()))
    async def bulk_checksum(self, paths, alg=None): return dict(await gather(*map(partial(self._checksum_helper, getcontext().MEMORY_MAPPED_IO_MANAGER_DEFAULT_CHECKSUM_ALG if alg is None else alg), paths)))
    async def bulk_copy(self, pairs): await gather(*starmap(self.copy_file, pairs))
    async def bulk_resize(self, sizes): await gather(*starmap(self._resize_helper, sizes.items()))
    async def compact_files(self, paths): await gather(*map(self._compact_helper, paths))
    async def find_in_files(self, pattern, paths, max_per_file=None, *, allow_overlapping=False):
        async def searchf(p, o):
            async with self.open(p) as f: return p, await (f.search if allow_overlapping else f.search_nonoverlapping)(pattern, o, max_per_file)
        return {k: v for k, v in await gather(*starmap(searchf, paths.items())) if v}
    P.patch_method_signatures((__init__, 'executor=None'), (prefetch_files, '*paths, init_size=0'), (_open, 'init_size, path, mode, /'))
del f, H, P, S, _, File, O