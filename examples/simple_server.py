import asyncio
from koa import Application

@asyncio.coroutine
def log_path(ctx, next):
  print('Got request. {}'.format(ctx.request))
  yield from next
  ctx.response.status = 200


@asyncio.coroutine
def log_headers(ctx, next):
  print('Headers: {}'.format(ctx.request.headers))
  yield from next


if __name__ == '__main__':
  app = Application()
  app.use(log_path)
  app.use(log_headers)

  app.listen(8000)
