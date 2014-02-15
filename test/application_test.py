import asyncio

from koa import Application
from koa.http import *
from itertools import repeat
from nose.tools import ok_
from unittest.mock import MagicMock

loop = asyncio.get_event_loop()

def create_context():
  m = MagicMock()
  req = HttpRequest(None)
  res = HttpResponse(m)
  return HttpContext(req, res)

def run_in_loop(app):
  loop.run_until_complete(app.on_request(create_context()))


def middleware_is_called_on_run_test():
  called = False

  @asyncio.coroutine
  def middleware(context, nxt):
    nonlocal called
    called = True

  app = Application()
  app.use(middleware)

  run_in_loop(app)

  ok_(called)


def middleware_exception_is_propagated_test():

  @asyncio.coroutine
  def middleware(ctx, nxt):
    raise ValueError('Time to stop')


  app = Application()
  app.use(middleware)

  try:
    run_in_loop(app)
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

  run_in_loop(app)

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
    run_in_loop(app)
  except ValueError:
    pass

  ok_(not md1_continued)

