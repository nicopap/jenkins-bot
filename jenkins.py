"""Defines interactions with jenkins."""
from os import system
import asyncio

from config import jenkins_conf, global_conf
import emulatejob
from reporter import collect_reports

# Prevents requesting continuous integration when the tests are already running
jenkins_lock = asyncio.Lock()

# XXX Warning: the 'system' call uses a user-provided string, this typically.v.
# is bad security and opens the system to trivial attacks. Make sure the
# config file is indeed written by yourself and do not contain any maliciously
# formed strings!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
async def request_continuous_integration(report_function, client):
    """Sends a request to jenkins to start analysing the code.
    Keeps a lock on the operation to prevent overloading the server."""
    print('[INFO] In request_continuous_integration.')
    if jenkins_lock.locked(): # abort if the operation is running
        print('[INFO] the jenkins job was locked, I won\'t send a request.')
        return
    else:
        await jenkins_lock.acquire()
    try:
        queue = await emulatejob.start(client)
        exitval = system(f'curl \'{global_conf.site}'
                        + f'{jenkins_conf.path}{jenkins_conf.tokenPath}?'
                        + f'job={jenkins_conf.project}'
                        + f'&token={jenkins_conf.token}\'')
        if exitval != 0:
            print('[ERROR] couldn\'t send to jenkins ci request.',
                  'maybe the server is down, or curl is not installed on the',
                  'system?')
            raise ConnectionError()
        await collect_reports(report_function)
    except:
        jenkins_lock.release()
        print('[WARNING] Some error occured, aborting continuous integration.')
        await emulatejob.abort(queue, client)
        raise
    jenkins_lock.release()
    url = f'{global_conf.site}{jenkins_conf.path}/job/{jenkins_conf.project}/'
    await emulatejob.stop(queue, client, url)

