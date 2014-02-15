import asyncio

from asyncio.protocols import Protocol
from asyncio.streams import StreamReader

from collections import OrderedDict

from http.client import responses as status_to_str

# try to import C parser then fallback in pure python parser.
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser


__all__ = ( 'HttpContext', 'HttpRequest', 'HttpResponse' )


class HttpContext:

  def __init__(self, request, response):
    self.request = request
    self.response = response


class HttpRequest:

  def __init__(self, reader, method='GET', url='/',
              version='1.0', query_string='', headers={}):
    self._reader = reader
    self.method = method
    self.url = url
    self.version = version
    self.headers = headers
    self.query_string = query_string


  @asyncio.coroutine
  def read(self, n=-1):
    yield from self._reader.read(n)


  @asyncio.coroutine
  def readexactly(self, n):
    yield from self._reader.readexactly(n)


  def __repr__(self):
    return '<HttpRequest {} {}>'.format(self.method, self.url)


class HttpResponse:

  def __init__(self, writer):
    self._writer = writer
    self._body = ''
    self.version = '1.0'
    self.status = 404
    self.headers = dict()


  def write(self, data=None):
    if not data or len(data) == 0: return

    if 'content-length' not in self.headers:
      self.headers['content-length'] = 0

    self.headers['content-length'] += len(data)
    self._body += data


  @asyncio.coroutine
  def _write_status_line(self):
    status_line = 'HTTP/{!s} {:d} {!s}\n'.format(
      self.version, self.status, status_to_str[self.status])

    self._writer.write(status_line.encode('latin-1'))

  @asyncio.coroutine
  def _write_headers(self):
    for (h, v) in self.headers.items():
      h = '-'.join([
        x.capitalize() for x in h.split('-') ])
      self._writer.write('{!s}: {!s}\n'.format(h, v).encode('latin-1'))

  @asyncio.coroutine
  def _write_body(self):
    if not self._body:
      print('Writing body')
      self._writer.write('\n\n'.encode('latin-1'))

  @asyncio.coroutine
  def end(self):
    yield from self._write_status_line()
    yield from self._write_headers()
    yield from self._write_body()


class HttpProtocol(Protocol):

  def __init__(self, app):
    self._app = app
    self._transport = None
    self._parser = None
    self._request = None

  def connection_made(self, transport):
    print('Connection Made')
    self._transport = transport
    pass


  def connection_lost(self, exc):
    print('Connection Lost')
    pass


  def pause_writing(self, exc):
    print('Pause Writing')
    pass

  def resume_writing(self):
    print('Resume Writing')
    pass

  def data_received(self, data):
    print('Data received {}'.format(data.decode('latin-1')))

    if not self._parser:
      self._parser = HttpParser()

    parser = self._parser

    parser.execute(data, len(data))

    if parser.is_headers_complete():
      print("Headers\n{}".format(parser.get_headers()))
      self._transport.pause_reading()

      reader = StreamReader()
      reader.set_transport(self._transport)

      request = HttpRequest(
          reader,
          method=parser.get_method(),
          url=parser.get_url(),
          query_string=parser.get_query_string(),
          version=parser.get_version(),
          headers=parser.get_headers())

      self._request = request

      ctx = HttpContext(request, HttpResponse(self._transport))
      f = asyncio.async(self._app.on_request(ctx))


    if parser.is_message_complete():
      print("Message complete")
      self._parser = None
      self._request = None
      self._transport.resume_reading()


  def eof_received(self):
    print('EOF received')
    pass


