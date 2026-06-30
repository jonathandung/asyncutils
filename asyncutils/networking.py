import asyncutils as A, asyncio as I
from sys import audit
from asyncutils._internal.py312 import Queue
from asyncutils._internal.helpers import LoopMixinBase, fullname
from asyncutils._internal.log import warning
from asyncutils._internal.submodules import networking_all as __all__
class LineProtocol(I.Protocol, LoopMixinBase):
    NEWLINE, CARRIAGE_RETURN, _h = __import__('os').linesep.encode(), b'\r', A.ignore_cancellation.combined(I.InvalidStateError); __slots__ = '__buf', '__cl', '__dw', '__er', '__lines', '__paused', 'transport'
    def __init__(self): audit(fullname(self)); self.__buf, self.__lines = bytearray(), Queue(); self.__cl = self.__paused = self.__er = False; self.transport = self.__dw = None
    @property
    def connected_transport(self):
        if (t := self.transport) is None: raise ConnectionError('asyncutils.networking.LineProtocol: no transport connected')
        return t
    def connection_made(self, transport): self.transport = transport
    def connection_lost(self, exc):
        if t := self.transport:
            with self._h: t.abort()
        self.__lines.shutdown(); self.__cl = True
        if w := self.__dw:
            if not w.done(): w.set_exception(ConnectionError('asyncutils.networking.LineProtocol: transport connection lost') if exc is None else exc)
            self.__dw = None
    def close(self):
        if t := self.transport:
            with self._h: t.close(); self.__cl = True
        return self.__cl
    def data_received(self, data, bufsize=None):
        if bufsize is None: bufsize = A.getcontext().LINE_PROTOCOL_DEFAULT_BUFFER_SIZE
        (b := self.__buf).extend(data); n = self.NEWLINE
        if len(b) > bufsize: self.flush()
        while not self.__cl and n in b: l, b = b.split(n, 1); self._put_line(l)
        self.__buf = b
        if self.__er: self.flush(); self.signal_eof()
    def flush(self): self._put_line(b := self.__buf); b.clear()
    def signal_eof(self): self.__lines.put_nowait(None)
    def pause_writing(self):
        self.__paused = True
        if self.__dw is None: self.__dw = self.make_fut()
    def resume_writing(self):
        self.__paused = False
        if w := self.__dw:
            if not w.done(): w.set_result(None)
            self.__dw = None
    def _put_line(self, data): self.__lines.put_nowait(data.rstrip(self.CARRIAGE_RETURN).decode('utf-8'))
    def write_line(self, line):
        with self._h:
            if not self.connected_transport.is_closing(): self.write_literal(line.encode('utf-8', 'ignore')+self.NEWLINE)
    def write_literal(self, data): self.connected_transport.write(data)
    def eof_received(self):
        self.__er = True
        if self.__buf: self.flush()
        if self.__lines.empty() and not self.__cl: self.signal_eof()
    async def read_line(self): L = self.__lines; return None if self.__cl and L.empty() else (L.task_done() if (l := await L.get()) is None else l)
    async def drain(self):
        if self.__paused and (w := self.__dw): await w
    async def write_line_with_backpressure(self, line): await self.drain(); self.write_line(line)
    async def write_literal_with_backpressure(self, data): await self.drain(); self.write_literal(data)
class LFProtocol(LineProtocol): NEWLINE, __slots__ = b'\n', ()
class CRLFProtocol(LineProtocol): NEWLINE, __slots__ = b'\r\n', ()
class CRProtocol(LineProtocol): NEWLINE, __slots__ = b'\r', ()
class SocketTransport(I.Transport):
    __slots__ = '__buf', '__cl', '__lim', '__protocol', '__sock'; _h = A.IgnoreErrors(OSError)
    @staticmethod
    def make_protocol(): return LineProtocol()
    @property
    def loop(self): return p.loop if isinstance(p := self.__protocol, LineProtocol) else NotImplemented
    def __init__(self, sock=None):
        audit(fullname(self)); self.__rx(); (p := self.make_protocol()).connection_made(self); self.__sock, self.__cl, self.__buf, self.__lim, self.__protocol = sock, False, bytearray(), A.getcontext().SOCKET_TRANSPORT_LIMITS, p
        if sock is not None: self.connect_sock(sock)
    def __rx(self, _=('socket', 'sockname', 'peername')): super().__init__(dict.fromkeys(_))
    def __rr(self, sock, size=None):
        try: self.__protocol.data_received(d) if (d := sock.recv(A.getcontext().LINE_PROTOCOL_DEFAULT_BUFFER_SIZE if size is None else size)) else (self.__protocol.eof_received() or self.close())
        except OSError as e: warning('%s: read error', fullname(self)); self.close(e)
    def connect_sock(self, sock=None):
        if sock is None and (sock := self.__sock) is None: return
        sock.setblocking(False); self.loop.add_reader(sock.fileno(), self.__rr, sock); (e := self._extra)['sockname'] = sock.getsockname() # ty: ignore[unresolved-attribute]
        with self._h: e['peername'] = sock.getpeername()
    def disconnect_sock(self):
        if (s := self.__sock) is None: return s
        with self._h: s.close()
        self.loop.remove_reader(s.fileno()); self.__sock = None; self.__rx(); return s
    @A.dualcontextmanager
    def sock_context(self, sock):
        try: yield self.connect_sock(sock)
        finally: self.disconnect_sock()
    def __writer(self, data, bufsize=None):
        if self.__cl: return
        (b := self.__buf).extend(data)
        if bufsize is None: bufsize = A.getcontext().SOCKET_TRANSPORT_LIMITS[1]
        if len(b) <= bufsize or (s := self.__sock) is None: return
        try: s.sendall(b); b.clear()
        except OSError as e: warning('%s: write error', fullname(self)); self.close(e)
    def write(self, data): self.loop.call_soon(self.__writer, data)
    def get_write_buffer_size(self): return len(self.__buf)
    def get_write_buffer_limits(self): return self.__lim
    def set_write_buffer_limits(self, high=None, low=None):
        l = self.__lim
        if low is None: low = l[0]
        if high is None: high = l[1]
        self.__lim = min(max(low, 0), high := min(high, A.getcontext().SOCKET_TRANSPORT_LIMITS[1])), high
    def write_eof(self):
        if not (self.__cl or (s := self.__sock) is None):
            with self._h: s.shutdown(1)
    def can_write_eof(self): return True # noqa: PLR6301
    def is_closing(self): return self.__cl
    def close(self, e=None):
        if self.__cl: return
        self.__cl = True; self.__protocol.connection_lost(e); self.disconnect_sock()
    def get_protocol(self): return self.__protocol
    def set_protocol(self, protocol):
        if not isinstance(protocol, LineProtocol): raise TypeError('asyncutils.networking.SocketTransport: protocol should be a LineProtocol')
        self.__protocol.connection_lost(None); protocol.connection_made(self); self.__protocol = protocol; self.connect_sock()
    def abort(self): self.loop.call_soon(self.close)
