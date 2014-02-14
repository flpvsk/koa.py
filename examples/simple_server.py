import asyncio
from koa import Application

@asyncio.coroutine
def log_path(ctx, next):
  print('Got request. {}'.format(ctx.request.url))
  yield from next
  print('Query String. {}'.format(ctx.request.query_string))


@asyncio.coroutine
def log_headers(ctx, next):
  print('Headers: {}'.format(ctx.request.headers))
  yield from next


if __name__ == '__main__':
  app = Application()
  app.use(log_path)
  app.use(log_headers)

  app.start(8000)
