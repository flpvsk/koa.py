import asyncio
import inspect

from asyncio.transports import WriteTransport
from koa.http import HttpResponse
from unittest.mock import MagicMock

loop = asyncio.get_event_loop()

class TestHttpResponse:

  def end_is_a_generator_test(self):
    writer = MagicMock(WriteTransport)
    res = HttpResponse(writer)
    result = res.end()

    assert inspect.isgenerator(result)


  def end_method_writes_status_line_test(self):
    writer = MagicMock(WriteTransport)
    res = HttpResponse(writer)
    res.status = 200

    loop.run_until_complete(res.end())

    writer.write.assert_any_call('HTTP/1.0 200 OK\n'.encode('latin-1'))


  def end_method_writes_content_length_test(self):
    writer = MagicMock(WriteTransport)
    res = HttpResponse(writer)
    res.status = 200

    response_str = 'Boo Ya!'
    res.write(response_str)

    loop.run_until_complete(res.end())

    status_str = 'Content-Length: {:d}\n'.format(len(response_str))
    writer.write.assert_called_with(status_str.encode('latin-1'))

  def end_method_no_body_test(self):
    buf = b''

    def write_to_buf(data):
      nonlocal buf
      buf += data

    writer = MagicMock(WriteTransport)
    writer.write = write_to_buf

    res = HttpResponse(writer)
    res.status = 200

    loop.run_until_complete(res.end())

    print('BUF', buf[-2:])

    assert buf[-2:] == b'\n\n'



class TestHttpProtocol:
  pass
