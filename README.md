### Koa.py

Web framework, inspired by [koa.js][koajs].

Started for exploring capabilities of python [asyncio][asyncio] framework.

Requires python 3.3 or higher.

Example:

    import asyncio
    from koa import Application

    @asyncio.coroutine
    def set_status(ctx, nxt):
      ctx.response.status = 200
      yield from nxt
      print('After write_body')


    @asyncio.coroutine
    def write_body(ctx, nxt):
      ctx.response.write('Hi, you\'ve reached {}'.format(ctx.request.url))
      yield from nxt


    if __name__ == '__main__':
      app = Application()
      app.use(set_status)
      app.use(write_body)

      app.listen(8000)

[koajs]: http://koajs.com/
[asyncio]: http://docs.python.org/3.4/library/asyncio.html
