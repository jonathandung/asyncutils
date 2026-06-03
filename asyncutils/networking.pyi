'''Some asyncio protocols and a transport. See :doc:`the asyncio documentation page <python:library/asyncio-protocol>`.'''
from ._internal.types import DualContextManager
from .mixins import LoopBoundMixin
from asyncio import AbstractEventLoop, Protocol, Transport, WriteTransport
from collections.abc import Iterable
from socket import socket
from typing import ClassVar, Literal
__all__ = 'CRLFProtocol', 'CRProtocol', 'LFProtocol', 'LineProtocol', 'SocketTransport'
class LineProtocol(Protocol, LoopBoundMixin):
    '''| An implementation of :class:`~asyncio.protocols.Protocol` providing line-based buffering and writing. Not thread-safe.
    | The idea was originally introduced in :pep:`3153`, but did not see eventual adaptation in the standard library.
    | This particular implementation is designed to be used with :class:`SocketTransport`, though other transports can enforce it too.
    | Instantiating this class will give an :class:`LFProtocol` or :class:`CRLFProtocol` depending on :data:`os.linesep`.'''
    NEWLINE: ClassVar[bytes]
    '''The newline sequence used by this protocol as bytes.'''
    CARRIAGE_RETURN: ClassVar[bytes]
    '''The carriage return sequence used by this protocol as bytes.'''
    @property
    def transport(self) -> WriteTransport|None: '''The transport associated with this protocol, or None if not connected.'''
    @property
    def connected_transport(self) -> WriteTransport: '''The transport associated with this protocol; raises :exc:`ConnectionError` if not connected.'''
    def connection_made(self, transport: WriteTransport) -> None: '''Unlike the base class, this method does not take read-only transports.''' # ty: ignore[invalid-method-override]
    def connection_lost(self, exc: Exception|None) -> None: '''Called when the connection is lost.'''
    def close(self) -> bool: '''Close the transport and return success.'''
    def data_received(self, data: bytes, bufsize: int=...) -> None: '''Called when some data is received, with `data` being a non-empty bytes object containing it.'''
    def flush(self) -> None: '''Flush the internal buffer and put in remaining data as a single line.'''
    def signal_eof(self) -> None: '''Signal that the stream is at EOF.'''
    def pause_writing(self) -> None: '''Called when the transport's buffer goes over the high watermark.'''
    def resume_writing(self) -> None: '''Called when the transport's buffer drains below the low watermark.'''
    def _put_line(self, data: bytes) -> None: '''Put the given `data` into the buffer as a single line.'''
    def write_line(self, line: str) -> None: '''Write the string `line` to the transport, followed by the newline sequence.'''
    def write_literal(self, data: bytes) -> None: '''Write the given bytes into the transport without appending a newline.'''
    def eof_received(self) -> None: '''Called when the other end signals it won't send any more data, for example by calling :meth:`Transport.write_eof`, which closes the transport.'''
    async def read_line(self) -> str|None: '''Read a line from the internal buffer and return it, or ``None`` if EOF is reached.'''
    async def drain(self) -> None: '''Wait until the transport is ready for more data to be written (i.e. the write buffer is flushed).'''
    async def write_line_with_backpressure(self, line: str) -> None: '''Write the string `line` to the transport, followed by the newline sequence, after draining it.'''
    async def write_literal_with_backpressure(self, data: bytes) -> None: '''Write the given bytes into the transport without appending a newline, after draining it.'''
class LFProtocol(LineProtocol): '''Line Feed protocol for Unix-like systems.'''
class CRLFProtocol(LineProtocol): '''Carriage Return + Line Feed protocol for Windows.'''
class CRProtocol(LineProtocol): '''Carriage Return protocol. For legacy systems no longer officially supported by python, such as Mac OS 9, such that this will never be chosen as the default.'''
class SocketTransport(Transport):
    '''A thread-unsafe transport that connects :class:`LineProtocol`'s to sockets.'''
    @staticmethod
    def make_protocol() -> LineProtocol: '''Return a new protocol compatible with this transport. The default implementation returns a :class:`LineProtocol`, so if overriding this in subclasses, remember to add `# type: ignore[override]` comments as appropriate.'''
    @property
    def loop(self) -> AbstractEventLoop: '''Override this if the type of the protocols this transport accepts is altered in subclasses.'''
    def __init__(self, sock: socket|None=...): '''Initialize the transport, connecting the socket immediately if given.'''
    def _reset_extra(self) -> None: ...
    def connect_sock(self, sock: socket=...) -> None: '''Connect the transport to the given socket.'''
    def disconnect_sock(self) -> socket|None: '''Disconnect the transport from its socket and return it, or ``None`` if not connected.'''
    def sock_context(self, sock: socket) -> DualContextManager[None]: '''Return a context manager, both sync and async, that connects the transport to the given socket on entry and disconnects it on exit.'''
    def write(self, data: Iterable[int]) -> None: '''Write the given iterable over integers in `range(256)` interpreted as characters into the transport.'''
    def get_write_buffer_size(self) -> int: '''Return the current size of the output buffer used by the transport.'''
    def get_write_buffer_limits(self) -> tuple[int, int]: '''Get the high and low watermarks for write flow control. Return a tuple `(low, high)`, where `low` and `high` are positive number of bytes.'''
    def set_write_buffer_limits(self, high: int|None=..., low: int|None=...) -> None: '''Set the high and low watermarks for write flow control in bytes.'''
    def write_eof(self) -> None: '''Close the write end of the transport after flushing all buffered data. Data may still be received.'''
    def can_write_eof(self) -> Literal[True]: '''Stub implementation that always returns ``True``.'''
    def is_closing(self) -> bool: '''Return whether the transport is closing or already closed.'''
    def close(self, e: Exception|None=...) -> None: '''Close the transport and flush the outgoing data buffer. No more data will be received. After all buffered data is flushed, the protocol's :meth:`connection_lost` method will be called with ``None`` as argument. The transport is not to be used once closed.'''
    def get_protocol(self) -> LineProtocol: '''Return the current protocol. For this class, it is expected to always be a :class:`LineProtocol` or one of its subclasses.'''
    def abort(self) -> None: '''Close the transport immediately, without waiting for pending operations to complete.'''