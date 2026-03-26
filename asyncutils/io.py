import sys
lazy from asyncio.tasks import eager_task_factory, gather
lazy from asyncio.locks import Lock
lazy from mmap import mmap
lazy from itertools import starmap
from _functools import partial # type: ignore
from contextlib import asynccontextmanager
from ._internal import helpers as H, patch as P
from .config import Executor
from .base import collect
from .util import sync_await
from .mixins import LoopContextMixin
from ._internal.submodules import io_all as __all__
if not (m := sys.modules.get('os')):
    N = sys.builtin_module_names
    for n in ('nt', 'posix'):
        if n in N: m = __import__(n); break
    else: raise ImportError('cannot find pipe and fsync implementations')
def f(a, b, m=m, /):
    def double_ended_pipe(pipe_impl=m.pipe, x=partial(open, mode=a), y=partial(open, mode=b)): r, W, R, w = *pipe_impl(), *pipe_impl(); r, R, w, W = *map(x, (r, R)), *map(y, (w, W)); sys.audit('asyncutils.io.double_ended_pipe', r, w, R, W); return AsyncReadWriteCouple(r, w), AsyncReadWriteCouple(R, W)
    return double_ended_pipe
_, I, s = lambda s=None, /, **d: {k: v for k, v in d.items() if v is not s}, sys.maxsize, '*, pipe_impl={}'
double_ended_text_pipe, double_ended_binary_pipe = t = tuple(map(f, ('r', 'rb'), ('w', 'wb')))
P.patch_function_signatures(*((_, s) for _ in t))
@H.subscriptable
class AsyncReadWriteCouple(LoopContextMixin):
    __slots__ = 'reader', 'writer', '_executor'
    def __init__(self, r, w, /): sys.audit('asyncutils/create_executor', 'io.AsyncReadWriteCouple'); super().__init__(); self.loop.set_task_factory(eager_task_factory); self.reader, self.writer, self._executor = r, w, Executor()
    async def _run(self, f, *a): return await self.loop.run_in_executor(self._executor, f, *a)
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
    def seek(self, offset, whence=0, /): raise OSError('cannot use seek on read-write couple')
    def tell(self): raise OSError('cannot use tell on read-write couple')
    def truncate(self, size=None, /): return self._run(self.writer.truncate, size)
    async def aclose(self): await gather(*map(self._run, (self.reader.close, self.writer.close))); self._executor.shutdown()
    __cleanup__ = aclose
    @property
    def closed(self): return self.reader.closed and self.writer.closed
    def __getattr__(self, name, /):
        try: return getattr(self.reader, name)
        except AttributeError as a:
            try: return getattr(self.writer, name)
            except AttributeError as b: raise ExceptionGroup(f'read-write couple has no attribute {name!r}', (a, b)) from None
class file(LoopContextMixin):
    __slots__ = '_f', '_fileno', 'mmap'
    if sys.platform != 'win32':
        def madvise(self, option, start=0, length=None, _filter=H.filter_out): return self.mmap.madvise(option, start, *_filter(length))
    async def reg(self, m, /):
        async with self.lock: self.mgr.add(m)
    async def unreg(self, m, /):
        async with self.lock: self.mgr.discard(m)
    def read(self, offset=0, size=-1): return self.run(self._read, offset, size)
    def write(self, data, offset=0): return self.run(self._write, data, offset)
    async def readline(self, offset=0, size=None, incl_newline=False): return (await self.run(self._readline, offset, size, incl_newline))[0]
    async def readlines(self, hint=-1): return list(await self.run(self._readlines, hint))
    async def flush(self, offset=0, size=None, /): return await self.run(self._flush, offset, size)
    def move(self, dest, src, count): return self.run(self._move, dest, src, count)
    async def __setup__(self): self.mmap = m = mmap(self._fileno, 0, access=2).__enter__(); await self.reg(m)
    async def __cleanup__(self): await gather(self.close(), self.unreg(self.mmap))
    def seek(self, pos, whence=0): return self.run(self.mmap.seek, pos, whence)
    def __new__(cls, file, /):
        if (r := cls.open_files.get((file, 'r+b'))) is None is (r := cls.open_files.get((file, 'w+b'))): (r := super().__new__(cls))._f, r._fileno = file, file.fileno()
        return r
    def __iter__(self): return self._f.__iter__()
    def __del__(self): self.loop.run_until_complete(self.close())
    @property
    def closed(self): return self._f.closed
    def fileno(self): return self._fileno
    def sync(self, _fsync=m.fsync): self._flush(0, None); _fsync(self._fileno)
    async def close(self): await gather(*map(self.run, (self.mmap.close, self._f.close)))
    def read_byte(self): return self.mmap.read_byte()
    def write_byte(self, b, /): self.mmap.write_byte(b)
    def resize(self, newsize): self.mmap.resize(newsize)
    def find(self, sub, start=None, end=None, _filter=_): return self.mmap.find(sub, **_filter(start=start, end=end))
    def rfind(self, sub, start=None, end=None, _filter=_): return self.mmap.rfind(sub, **_filter(start=start, end=end))
    def tell(self): return self.mmap.tell()
    def size(self): return self.mmap.size()
    def isatty(self): return self._f.isatty()
    readable = writable = seekable = lambda _, /: True
    def _flush(self, offset, size, _filter=H.filter_out): self._f.flush(); self.mmap.flush(offset, *_filter(size))
    def _move(self, dest, src, count): self.mmap.move(dest, src, count)
    def _trunc_from(self, data, offset): c = (m := self.mmap).tell(); m.seek(0, 2); m.resize(max(m.tell(), x := offset+len(data))); m.seek(c); return x
    def _read(self, offset, size): return self.mmap[offset:None if size < 0 else offset+size]
    def _write(self, data, offset): (m := self.mmap)[offset:self._trunc_from(data, offset)] = data; m.flush()
    def _readline(self, offset, size, incl_newline): return (b'', 0) if offset >= (l := len(m := self.mmap)) else (m[offset:(q := p if (e := m.find(b'\n', offset, p := (l if size is None else min(offset+size, l)))) == -1 else e+incl_newline)], q)
    def _readlines(self, hint, /):
        if hint < 0: yield from map(bytes, self.mmap)
        else:
            while hint > 0: b, n = self._readline(0, hint, False); yield b; hint -= n
    async def writelines(self, lines, /, *, sep=b''):
        for l in lines: await self.write(l+sep)
    async def read_str(self, offset=0, size=-1, encoding='utf-8', errors='strict'): return (await self.read(offset, size)).decode(encoding, errors)
    def write_str(self, text, offset=0, encoding='utf-8', errors='strict'): return self.write(text.encode(encoding, errors), offset)
    def smart_write(self, data, offset=0): return self.write(data.encode('utf-8', 'replace') if isinstance(data, str) else data, offset)
    async def copy_range(self, src_offset, dest_offset, size):
        try: await self.write(await self.read(src_offset, size), dest_offset); return True
        except: return False
    def fill(self, pattern, offset=0, count=1): return self.write(pattern*count, offset)
    async def compare(self, other, /, size=-1, offset_self=0, offset_other=0): return (await self.read(offset_self, size)) == (await other.read(offset_other, size))
    async def hamming_dist(self, other, /, size=-1, offset_self=0, offset_other=0): return sum(x.bit_count() for x in map(int.__xor__, await self.read(offset_self, size), await other.read(offset_other, size), strict=size>0))
    async def read_until(self, delim, offset=0, maxsize=-1): return (d, offset+len(d)) if (p := (d := await self.read(offset, maxsize)).find(delim)) == -1 else (d[:p+(l := len(delim))], offset+p+l)
    async def insert(self, data, offset): await self.write(data if offset > await self.run(self.size) else data+await self.read(offset), offset)
    async def delete(self, offset, size):
        if size <= 0 or offset >= (s := await self.run(self.mmap.size)): return
        if (t := offset+size) < s: await self.write(await self.read(t), offset)
        await self.run(self.resize, max(0, s-size))
    async def replace(self, old, new, offset=0, count=I):
        r, c, o, n = 0, offset, len(old), len(new)
        while r < count:
            if (p := await self.run(self.find, old, c)) == -1: break
            await self.delete(p, o); await self.insert(new, p); r += 1; c = p+n
        return r
    async def search_lazy(self, pattern, offset=0, max_results=I):
        for c in range(offset, offset+max_results):
            if (p := await self.run(self.find, pattern, c)) == -1: break
            yield p
    async def search_lazy_nonoverlapping(self, pattern, offset=0, max_results=I):
        for _ in range(max_results):
            if (offset := await self.run(self.find, pattern, offset)) == -1: break
            yield offset
    def search(self, pattern, offset=0, max_results=I): return collect(self.search_lazy(pattern, offset, max_results))
    def search_nonoverlapping(self, pattern, offset=0, max_results=I): return collect(self.search_lazy_nonoverlapping(pattern, offset, max_results))
    async def compact(self):
        for i in range(len(c := await self.read())-1, -1, -1):
            if c[i]: await self.run(self.resize, i+1); break
    def __init_subclass__(cls, *, m, l, r, e):
        @staticmethod
        async def run(f, /, *a, r=r): return await r(f, *a)
        @staticmethod
        def exit(*_): return e()
        cls.mgr, cls.lock, cls.run, cls.exit, cls.open_files = m, l, run, exit, {}
class MemoryMappedIOManager(LoopContextMixin):
    __slots__ = '_factory'
    def __init__(self, executor=None, _=file):
        if executor is None: sys.audit('asyncutils/create_executor', 'channels.MemoryMappedIOManager'); executor = Executor()
        super().__init__(); self._factory = type('file', (_,), {}, m=__import__('_weakrefset').WeakSet(), l=Lock(), r=partial(self.loop.run_in_executor, executor), e=self.exiter)
    @property
    def open_mmaps(self): return self._factory.mgr
    @property
    def _lock(self): return self._factory.lock
    def _run(self, f, /, *a): return self._factory.run(f, *a)
    @property
    def currently_open(self): return len(self.open_mmaps)
    @property
    def open_paths(self): return dict(self.open_files.keys())
    @property
    def open_files(self): return self._factory.open_files
    @open_files.setter
    def open_files(self, val: dict, /): self._factory.open_files = val
    @open_files.deleter
    def open_files(self): self.open_files.clear()
    @asynccontextmanager
    async def _open(self, init_size, *k):
        if (x := self.open_files.get(k)): yield x; return
        try:
            with open(*k) as f:
                if init_size > 0: await self._run(f.truncate, init_size)
                async with self._factory(f) as x: self.open_files[k] = x; yield x # type: ignore
        finally: self.open_files.pop(k, None)
    def open(self, path, init_size=0): return self._open(init_size, path, 'r+b')
    def create(self, path, init_size=0): return self._open(init_size, path, 'w+b')
    async def __cleanup__(self):
        async with self._lock: self.open_mmaps.clear(); await gather(*(f.close() for f in self.open_files.values())); self.open_files.clear()
    def __del__(self): sync_await(self.__cleanup__(), loop=(l := self.loop)); l.stop(); l.close()
    async def copy_file(self, srcp, destp):
        async with self.open(srcp) as src, self.create(destp) as dest: await dest.write(await src.read()); await dest.flush()
    async def checksum(self, path, alg='md5'):
        async with self.open(path) as f: return __import__('hashlib').new(alg, await f.read()).hexdigest()
    async def approx_memory_usage(self):
        async with self._lock: return await self._run(lambda: sum(m.size() for m in self.open_mmaps))
    @asynccontextmanager
    async def prefetch_files(self, *P, init_size=0):
        try: l = tuple(self.open(p, init_size) for p in P); yield await gather(*(c.__aenter__() for c in l))
        finally: t = sys.exc_info(); await gather(*(c.__aexit__(*t) for c in l))
    @asynccontextmanager
    async def create_sparsef(self, path, total_size, chunks):
        async with self.create(path, total_size) as f:
            for o, d in chunks.items(): await f.smart_write(d, o)
            yield f
    async def _bulk_reader(self, path, offsets):
        r = []
        async with self.open(path) as f:
            for o, s in offsets: r.append(await f.read(o, s))
            return path, r
    async def _bulk_writer(self, path, data):
        async with self.open(path) as f: await gather(*(f.write(d, o) for d, o in data))
    async def _checksum_helper(self, path, alg='md5'): return path, await self.checksum(path, alg)
    async def _resize_helper(self, path, size):
        async with self.open(path) as f: await self._run(f.resize, size)
    async def _compact_helper(self, path):
        async with self.open(path) as f: await f.compact()
    async def bulk_read(self, file_offsets): return dict(await gather(*(self._bulk_reader(*_) for _ in file_offsets.items())))
    async def bulk_write(self, file_data): await gather(*(self._bulk_writer(*_) for _ in file_data.items()))
    async def bulk_checksum(self, paths, alg='md5'): return dict(await gather(*map(partial(self._checksum_helper, alg=alg), paths)))
    async def bulk_copy(self, pairs): await gather(*(self.copy_file(*p) for p in pairs))
    async def bulk_resize(self, sizes): await gather(*(self._resize_helper(*t) for t in sizes.items()))
    async def compact_files(self, paths): await gather(*map(self._compact_helper, paths))
    async def find_in_files(self, pattern, paths, max_per_file=I, *, allow_overlapping=False):
        async def searchf(p, o):
            async with self.open(p) as f: return p, await (f.search if allow_overlapping else f.search_nonoverlapping)(pattern, o, max_per_file)
        return {k: v for k, v in await gather(*starmap(searchf, paths.items())) if v}
del f, H, P, _, m, I, file