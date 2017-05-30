from config import hooks_conf
from webhooklistener import subscribe_to, unsubscribe_from

def react_to_github(json_data):
    """Launch the jenkins server ci process based on a git hook."""
    print('Github hook was recieved')
    print(json_data)

def listen_to_github(report_function):
    """Setups the structure to listen to github hooks."""
    subscribe_to(hooks_conf.githubPath, react_to_github)
