import asyncio
from asyncio.protocols import Protocol
from asyncio.streams import StreamReader

# try to import C parser then fallback in pure python parser.
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser


class HttpContext():

  def __init__(self, request, response):
    self.request = request
    self.response = response


class HttpRequest():

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

      ctx = HttpContext(request, None)
      self._app.on_request(ctx)

    if parser.is_message_complete():
      print("Message complete")
      self._parser = None
      self._request = None
      self._transport.resume_reading()


  def eof_received(self):
    print('EOF received')
    pass
