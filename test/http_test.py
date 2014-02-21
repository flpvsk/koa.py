import asyncio
import inspect

from asyncio.transports import WriteTransport
from koa.http import HttpResponse
from unittest.mock import MagicMock

loop = asyncio.get_event_loop()

class TestHttpResponse:

  def setUp(self):
    self._result = b''
    self._writer = MagicMock(WriteTransport)

    def write_to_result(data):
      self._result += data

    def write_line_to_result(data):
      self._result += data
      self.result += b'\n'

    self._writer.write = write_to_result
    self._writer.writeline = write_line_to_result


  def end_is_a_generator_test(self):
    writer = MagicMock(WriteTransport)
    res = HttpResponse(writer)
    result = res.end()

    assert inspect.isgenerator(result)


  def end_method_writes_status_line_test(self):
    res = HttpResponse(self._writer)
    res.status = 200

    loop.run_until_complete(res.end())

    assert self._result.index(b'HTTP/1.0 200 OK\n') == 0


  def end_method_writes_content_length_test(self):
    res = HttpResponse(self._writer)

    res.status = 200
    response_str = 'Boo Ya!'
    response_len_b = bytes(str(len(response_str)), 'latin-1')
    res.write(response_str)

    loop.run_until_complete(res.end())

    status_str = b'Content-Length: ' + response_len_b + b'\n'
    assert status_str in self._result

  def end_method_no_body_test(self):
    res = HttpResponse(self._writer)

    loop.run_until_complete(res.end())

    assert self._result[-2:] == b'\n\n'


  def write_body_test(self):
    res = HttpResponse(self._writer)

    res.status = 200
    res.write('Response body!')

    loop.run_until_complete(res.end())

    print('RESULT:', self._result)
    assert b'\n\nResponse body!\n\n' in self._result


  def headers_are_case_insensitive_test(self):
    res = HttpResponse(self._writer)
    res.headers['x-mY-hEadEr'] = 'my-value'

    loop.run_until_complete(res.end())

    assert b'X-My-Header: my-value' in self._result


  def headers_insensitive_override_test(self):
    res = HttpResponse(self._writer)

    res.headers['x-my-header'] = 'old-value'
    res.headers['X-My-Header'] = 'new-value'

    loop.run_until_complete(res.end())

    print("RESULT ***", self._result)

    assert b'X-My-Header: new-value' in self._result
    assert b'old-value' not in self._result

