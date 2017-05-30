"""Actions to prosecute when a jenkins job is launched"""
from time import sleep

from config import hooks_conf
from webhooklistener import subscribe_to, unsubscribe_from

def expect_hook(timeout, path, to_call):
    """Subscribes to a request on the given path, with timeout."""
    subscribe_to(path, to_call)
    sleep(timeout)
    unsubscribe_from(path)
    raise TimeoutError()

def collect_reports(report_function):
    """Turns the bot in state of expecting hooks from the continuous
    integration structure and sends the content of the hooks to
    report_function"""
    print('[INFO] in collect_reports, setting up expectation hooks.')
    expect_hook(hooks_conf.timeout, hooks_conf.sonarPath, report_function)
    expect_hook(hooks_conf.timeout, hooks_conf.sonarPath, report_function)

