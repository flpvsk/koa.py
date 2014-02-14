import asyncio

from koa import Application
from itertools import repeat
from nose.tools import ok_

def middleware_is_called_on_run_test():
  called = False

  @asyncio.coroutine
  def middleware(context, nxt):
    nonlocal called
    called = True

  app = Application()
  app.use(middleware)
  app.run()

  ok_(called)


def middleware_exception_is_propagated_test():

  @asyncio.coroutine
  def middleware(ctx, nxt):
    raise ValueError('Time to stop')


  app = Application()
  app.use(middleware)

  try:
    app.run()
    raise AssertionError('Exception not thrown')
  except ValueError as e:
    pass


def more_than_one_middleware_test():
  called = set()

  def make_middleware(id):

    @asyncio.coroutine
    def md(ctx, nxt):
      called.add(id)
      yield from nxt

    return md


  app = Application()

  for id in range(10):
    app.use(make_middleware(id))

  app.run()

  for id in range(10):
    ok_(id in called, '{} not in {}'.format(id, called))





def execution_stops_if_error_test():
  md1_continued = False

  @asyncio.coroutine
  def md1(ctx, nxt):
    nonlocal md1_continued
    yield from nxt
    md1_continued = True



  @asyncio.coroutine
  def md2(ctx, nxt):
    raise ValueError('Stop!')


  app = Application()

  app.use(md1)
  app.use(md2)

  try:
    app.run()
  except ValueError:
    pass

  ok_(not md1_continued)


