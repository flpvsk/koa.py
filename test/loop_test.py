import asyncio


loop = asyncio.get_event_loop()


def callback_test():
    future = asyncio.Future()
    callback_called = False

    def set_future_result():
        future.set_result(None)

    def on_future_complete(f):
        nonlocal callback_called
        callback_called = True
    future.add_done_callback(on_future_complete)

    loop.call_soon(set_future_result)
    loop.run_until_complete(future)

    assert callback_called



def coroutine_test():
    future = asyncio.Future()

    callback_called = False

    def set_future_result():
        future.set_result(None)

    @asyncio.coroutine
    def on_future_result():
        nonlocal callback_called
        x = yield from future
        callback_called = True

    on_future_result = on_future_result()

    loop.call_soon(on_future_result)
    loop.call_soon(set_future_result)
    loop.run_until_complete(on_future_result)
