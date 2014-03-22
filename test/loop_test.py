import asyncio


loop = asyncio.get_event_loop()


def read_data_from(name):
    waiter = asyncio.Future()
    loop.call_later(.1, waiter.set_result, "Data from {}".format(name))
    return waiter


def read_one_source_cb_test():
    result = ""

    def on_data(future):
        nonlocal result
        result = future.result()
        loop.stop()

    def read_and_process():
        read_data_from('file').add_done_callback(on_data)

    loop.call_soon(read_and_process)
    loop.run_forever()

    assert result == 'Data from file', "%r is not expected" % result


def read_one_source_co_test():
    result = ""

    @asyncio.coroutine
    def read_and_process():
        nonlocal result
        result = yield from read_data_from('file')

    task = asyncio.Task(read_and_process())
    loop.call_soon(task)
    loop.run_until_complete(task)

    assert result == 'Data from file', "%r is not expected" % result


def read_two_sources_sequentially_cb_test():
    result = ""

    def on_data_2(future):
        nonlocal result
        result += "Content2: %s" % future.result()
        loop.stop()

    def on_data_1(future):
        nonlocal result
        result += "Content1: %s\n" % future.result()
        read_data_from('file2').add_done_callback(on_data_2)

    def read_and_process():
        read_data_from('file1').add_done_callback(on_data_1)

    loop.call_soon(read_and_process)
    loop.run_forever()

    expected = "Content1: Data from file1\nContent2: Data from file2"
    assert result == expected, "%r not expected" % result


def read_two_sources_sequentially_co_test():
    result = ""

    def read_and_process():
        nonlocal result
        content1 = yield from read_data_from('file1')
        content2 = yield from read_data_from('file2')
        result = "Content1: %s\nContent2: %s" % (content1, content2)

    task = asyncio.Task(read_and_process())
    loop.call_soon(task)
    loop.run_until_complete(task)

    expected = "Content1: Data from file1\nContent2: Data from file2"
    assert result == expected, "%r not expected" % result


def read_two_sources_parallel_cb_test():
    result = ""

    def on_data_2(future):
        nonlocal result
        result += "Content2: %s" % future.result()
        loop.stop()

    def on_data_1(future):
        nonlocal result
        result += "Content1: %s\n" % future.result()

    def read_and_process():
        read_data_from('file1').add_done_callback(on_data_1)
        read_data_from('file2').add_done_callback(on_data_2)

    loop.call_soon(read_and_process)
    loop.run_forever()

    expected = "Content1: Data from file1\nContent2: Data from file2"
    assert result == expected, "%r not expected" % result



def read_two_source_parallel_co_test():
    result = ""

    def read_and_process():
        nonlocal result
        content = asyncio.gather(
                read_data_from('file1'),
                read_data_from('file2'))
        content1, content2 = yield from content
        result = "Content1: %s\nContent2: %s" % (content1, content2)

    task = asyncio.Task(read_and_process())
    loop.call_soon(task)
    loop.run_until_complete(task)

    expected = "Content1: Data from file1\nContent2: Data from file2"
    assert result == expected, "%r not expected" % result

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
