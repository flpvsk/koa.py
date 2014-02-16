import asyncio

from koa.http import HttpProtocol

__all__ = ( 'Application', )

@asyncio.coroutine
def stop():
  pass

STOP = stop()

class Application():

  def __init__(self, loop=asyncio.get_event_loop()):
    self._middleware_list = []
    self._loop = loop


  def use(self, middleware):
    self._middleware_list.append(middleware)


  @asyncio.coroutine
  def on_request(self, ctx):
    mw_list = self._middleware_list

    if not mw_list:
      return

    prev = mw_list[-1](ctx, STOP)

    for mw in mw_list[-2::-1]:
      cur = mw(ctx, prev)
      prev = cur

    first = prev

    yield from first
    yield from ctx.response.end()


  def listen(self, port=8000):

    def protocol_factory():
      return HttpProtocol(self)

    server = loop.create_server(
          protocol_factory, host='127.0.0.1', port=port)

    loop.run_until_complete(server)
    print('Server started on port {}'.format(port))
    loop.run_forever()
