"""Actions to prosecute when a jenkins job is launched"""
import asyncio
from queue import Queue

from config import hooks_conf
from webhooklistener import subscribe_to, unsubscribe_from

HAS_CALLED_MSG=1

async def expect_hook(path, to_call):
    """Subscribes to a request on the given path, with timeout."""
    print('[INFO] in expect_hook')
    queue = Queue()
    async def notify_call(json_content):
        await to_call(json_content)
        queue.put(HAS_CALLED_MSG)
    async def wait_two_msg():
        queue.get()
        queue.get()
    subscribe_to(path, notify_call)
    try:
        await asyncio.wait_for(wait_two_msg(), hooks_conf.timeout)
    except asyncio.TimeoutError:
        print('[WARNING] the sonar summaries were timed out in expect_hook')
    else:
        print('[INFO] the two sonar summaries were recieved in time in expect_hook')
    finally:
        unsubscribe_from(path)

async def collect_reports(report_function):
    """Turns the bot in state of expecting hooks from the continuous
    integration structure and sends the content of the hooks to
    report_function"""
    print('[INFO] in collect_reports, setting up expectation hooks.')
    await expect_hook(hooks_conf.sonarPath, report_function)
