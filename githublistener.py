"""Listen and reacts to github events."""
from config import hooks_conf, jenkins_conf
import jenkins
from webhooklistener import subscribe_to, unsubscribe_from

def listen_to_github(report_function, client):
    """Setups the structure to listen to github hooks."""
    async def react_to_github(json_data):
        """Launch the jenkins server ci process based on a git hook."""
        print('[INFO] Github hook was recieved')
        pushed_branch = json_data['ref'].split('/')[-1]
        if pushed_branch == jenkins_conf.cibranch:
            await jenkins.request_continuous_integration(report_function, client)
    subscribe_to(hooks_conf.githubPath, react_to_github)
