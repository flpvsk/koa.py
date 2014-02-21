import asyncio
from koa import Application

@asyncio.coroutine
def log_path(ctx, nxt):
  print('Got request. {}'.format(ctx.request))
  yield from nxt


@asyncio.coroutine
def log_headers(ctx, nxt):
  print('Headers: {}'.format(ctx.request.headers))
  yield from nxt


@asyncio.coroutine
def say_hello(ctx, nxt):
  ctx.response.status = 200
  ctx.response.write('Hello, you\'ve reached {}'.format(ctx.request.url))
  yield from nxt


if __name__ == '__main__':
  app = Application()
  app.use(log_path)
  app.use(log_headers)
  app.use(say_hello)

  app.listen(8000)
