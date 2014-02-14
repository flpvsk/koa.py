### Koa.py

Web framework, inspired by [koa.js][koajs].

Started for exploring capabilities of python [asyncio][asyncio] framework.

Requires python 3.3 or higher.

Example:

    import asyncio
    from koa import Application

    @asyncio.coroutine
    def md1(ctx, next):
      print('Before md2')
      print('Url: {}'.format(ctx.request.url))
      yield from next
      print('After md2')


    @asyncio.coroutine
    def md2(ctx, next):
      print('md2')
      yield from next


    if __name__ == '__main__':
      app = Application()
      app.use(md1)
      app.use(md2)

      app.listen(8000)

[koajs]: http://koajs.com/
[asyncio]: http://docs.python.org/3.4/library/asyncio.html
