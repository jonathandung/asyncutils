import asyncutils as A, asyncio as I
from sys import audit
from asyncutils._internal.py312 import Queue
from asyncutils._internal.helpers import LoopMixinBase, fullname
from asyncutils._internal.log import warning
from asyncutils._internal.submodules import networking_all as __all__
class LineProtocol(I.Protocol, LoopMixinBase):
    NEWLINE, CARRIAGE_RETURN, _h = __import__('os').linesep.encode(), b'\r', A.ignore_cancellation.combined(I.InvalidStateError); __slots__ = '_buffer', '_closed', '_drain_waiter', '_eof_received', '_lines', '_paused', 'transport'
    def __init__(self): audit(fullname(self)); self._buffer, self._lines = bytearray(), Queue(); self._closed = self._paused = self._eof_received = False; self.transport = self._drain_waiter = None
    @property
    def connected_transport(self):
        if (t := self.transport) is None: raise ConnectionError('asyncutils.networking.LineProtocol: no transport connected')
        return t
    def connection_made(self, transport): self.transport = transport
    def connection_lost(self, exc):
        if t := self.transport:
            with self._h: t.abort()
        self._lines.shutdown(); self._closed = True
        if w := self._drain_waiter:
            if not w.done(): w.set_exception(ConnectionError('asyncutils.networking.LineProtocol: transport connection lost') if exc is None else exc)
            self._drain_waiter = None
    def close(self):
        if t := self.transport:
            with self._h: t.close(); self._closed = True
        return self._closed
    def data_received(self, data, bufsize=None):
        if bufsize is None: bufsize = A.getcontext().LINE_PROTOCOL_DEFAULT_BUFFER_SIZE
        (b := self._buffer).extend(data); n = self.NEWLINE
        if len(b) > bufsize: self.flush()
        while not self._closed and n in b: l, b = b.split(n, 1); self._put_line(l)
        self._buffer = b
        if self._eof_received: self.flush(); self.signal_eof()
    def flush(self): self._put_line(b := self._buffer); b.clear()
    def signal_eof(self): self._lines.put_nowait(None)
    def pause_writing(self):
        self._paused = True
        if self._drain_waiter is None: self._drain_waiter = self.make_fut()
    def resume_writing(self):
        self._paused = False
        if w := self._drain_waiter:
            if not w.done(): w.set_result(None)
            self._drain_waiter = None
    def _put_line(self, data): self._lines.put_nowait(data.rstrip(self.CARRIAGE_RETURN).decode('utf-8'))
    def write_line(self, line):
        with self._h:
            if not self.connected_transport.is_closing(): self.write_literal(line.encode('utf-8', 'ignore')+self.NEWLINE)
    def write_literal(self, data): self.connected_transport.write(data)
    def eof_received(self):
        self._eof_received = True
        if self._buffer: self.flush()
        if self._lines.empty() and not self._closed: self.signal_eof()
    async def read_line(self): L = self._lines; return None if self._closed and L.empty() else (L.task_done() if (l := await L.get()) is None else l)
    async def drain(self):
        if self._paused and (w := self._drain_waiter): await w
    async def write_line_with_backpressure(self, line): await self.drain(); self.write_line(line)
    async def write_literal_with_backpressure(self, data): await self.drain(); self.write_literal(data)
class LFProtocol(LineProtocol): NEWLINE, __slots__ = b'\n', ()
class CRLFProtocol(LineProtocol): NEWLINE, __slots__ = b'\r\n', ()
class CRProtocol(LineProtocol): NEWLINE, __slots__ = b'\r', ()
class SocketTransport(I.Transport):
    __slots__ = '_buffer', '_closing', '_limits', '_protocol', '_socket'; _h = A.IgnoreErrors(OSError)
    @staticmethod
    def make_protocol(): return LineProtocol()
    @property
    def loop(self): return p.loop if isinstance(p := self._protocol, LineProtocol) else NotImplemented
    def __init__(self, sock=None):
        audit(fullname(self)); self.__rx(); (p := self.make_protocol()).connection_made(self); self._socket, self._closing, self._buffer, self._limits, self._protocol = sock, False, bytearray(), A.getcontext().SOCKET_TRANSPORT_LIMITS, p
        if sock is not None: self.connect_sock(sock)
    def __rx(self, _=('socket', 'sockname', 'peername')): super().__init__(dict.fromkeys(_))
    def __rr(self, sock, size=None):
        try: self._protocol.data_received(d) if (d := sock.recv(A.getcontext().LINE_PROTOCOL_DEFAULT_BUFFER_SIZE if size is None else size)) else (self._protocol.eof_received() or self.close())
        except OSError as e: warning('%s: read error', fullname(self)); self.close(e)
    def connect_sock(self, sock=None):
        if sock is None and (sock := self._socket) is None: return
        sock.setblocking(False); self.loop.add_reader(sock.fileno(), self.__rr, sock); (e := self._extra)['sockname'] = sock.getsockname() # ty: ignore[unresolved-attribute]
        with self._h: e['peername'] = sock.getpeername()
    def disconnect_sock(self):
        if (s := self._socket) is None: return s
        with self._h: s.close()
        self.loop.remove_reader(s.fileno()); self._socket = None; self.__rx(); return s
    @A.dualcontextmanager
    def sock_context(self, sock):
        try: yield self.connect_sock(sock)
        finally: self.disconnect_sock()
    def __writer(self, data, bufsize=None):
        if self._closing: return
        (b := self._buffer).extend(data)
        if bufsize is None: bufsize = A.getcontext().SOCKET_TRANSPORT_LIMITS[1]
        if len(b) <= bufsize or (s := self._socket) is None: return
        try: s.sendall(b); b.clear()
        except OSError as e: warning('%s: write error', fullname(self)); self.close(e)
    def write(self, data): self.loop.call_soon(self.__writer, data)
    def get_write_buffer_size(self): return len(self._buffer)
    def get_write_buffer_limits(self): return self._limits
    def set_write_buffer_limits(self, high=None, low=None):
        l = self._limits
        if low is None: low = l[0]
        if high is None: high = l[1]
        self._limits = min(max(low, 0), high := min(high, A.getcontext().SOCKET_TRANSPORT_LIMITS[1])), high
    def write_eof(self):
        if not (self._closing or (s := self._socket) is None):
            with self._h: s.shutdown(1)
    def can_write_eof(self): return True # noqa: PLR6301
    def is_closing(self): return self._closing
    def close(self, e=None):
        if self._closing: return
        self._closing = True; self._protocol.connection_lost(e); self.disconnect_sock()
    def get_protocol(self): return self._protocol
    def set_protocol(self, protocol):
        if not isinstance(protocol, LineProtocol): raise TypeError('asyncutils.networking.SocketTransport: protocol should be a LineProtocol')
        self._protocol.connection_lost(None); protocol.connection_made(self); self._protocol = protocol; self.connect_sock()
    def abort(self): self.loop.call_soon(self.close)
