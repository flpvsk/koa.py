import asyncio


@asyncio.coroutine
def middleware1(nxt):
  print("Before Md1")
  yield from nxt
  print("After Md1")


@asyncio.coroutine
def middleware2(nxt):
  print("Before Md2")
  yield from nxt
  print("After Md2")

@asyncio.coroutine
def stop():
  pass

STOP = stop()

def run(*args):
  if not args:
    return

  prev = args[-1](STOP)

  for md in args[-2::-1]:
    cur = md(prev)
    prev = cur

  first = prev
  while True:
    try:
      next(first)
    except StopIteration:
      return

if __name__ == '__main__':
  run(middleware1, middleware2)
  print('Done')
