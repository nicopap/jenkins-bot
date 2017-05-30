"""Defines interactions with jenkins."""
from os import system
from http import client
from asyncio import Lock

from config import jenkins_conf
from reporter import collect_reports

# Prevents requesting continuous integration when the tests are already running.
jenkins_lock = Lock()

# XXX Warning: the 'system' call uses a user-provided string, this typically.v.
# is bad security and opens the system to trivial attacks. Make sure the
# config file is indeed written by yourself and do not contain any maliciously
# formed strings!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
async def request_continuous_integration(report_function):
    """Sends a request to jenkins to start analysing the code.
    Keeps a lock on the operation to prevent overloading the server."""
    print("[INFO] In request_continuous_integration, connecting to jenkins.")
    if jenkins_lock.locked(): # abort if the operation is running
        return
    else:
        await jenkins_lock.acquire()
    try:
        exitval = system(f'curl \'{jenkins_conf.site}{jenkins_conf.path}?job={jenkins_conf.project}&token={jenkins_conf.token}\'')
        if exitval != 0:
            raise ConnectionError()
        collect_reports(report_function)
    except:
        jenkins_lock.release()
        print("[INFO] Some error occured, aborting continuous integration.")
        raise

