import asyncio

from koa.http import HttpProtocol

__all__ = ( 'Application', )

@asyncio.coroutine
def stop():
  pass

STOP = stop()

class Application():

  def __init__(self):
    self._middleware_list = []


  def use(self, middleware):
    self._middleware_list.append(middleware)


  def on_request(self, ctx):
    self.run(ctx)


  def run(self, ctx=None):
    mw_list = self._middleware_list

    if not mw_list:
      return

    prev = mw_list[-1](ctx, STOP)

    for mw in mw_list[-2::-1]:
      cur = mw(ctx, prev)
      prev = cur

    first = prev
    while True:
      try:
        next(first)
      except StopIteration:
        return


  def listen(self, port=8000, loop=asyncio.get_event_loop()):

    def protocol_factory():
      return HttpProtocol(self)

    server = loop.create_server(
          protocol_factory, host='127.0.0.1', port=port)

    loop.run_until_complete(server)
    print('Server started on port {}'.format(port))
    loop.run_forever()
