"""Reads the configuaration file for initialisation constants

The configuration file is bot.config, it follows the classical Windows INI
file format. It has the following sections:

[hooks]:
The webhooks paths to listen to, for the bottle server
    sonarPath: The path that sonar will request when activating a webhook
    githubPath: The path that github will request when activating a webhook
    timeout: How long (in seconds) should the bot wait the sonar report
        until it assumes it simply wont ever answer.

[jenkins]:
Jenkins ci related settings
    token: The token to use to authenticate for jenkins
    path: the path to use to trigger the build of the project
    site: the domain name of the jenkins instance
    project: The project that must be built

[discord]:
The discord related settings
    token: The discord token key, to use the bot account.
    activateId: The channel where we recieve commands from.
    reportId: the channel in which to post reports.
    masterId: The user with extra privileges.
    trigger: The message that triggers the Jenkins ci job.
"""
import configparser
from collections import namedtuple

Hooks_conf = namedtuple('Hooks_conf', ['sonarPath', 'githubPath', 'timeout'])
Jenkins_conf = namedtuple('Jenkins_conf', ['token', 'path', 'site', 'project'])
Discord_conf = namedtuple('Discord_conf', ['token', 'activateId',
                                           'reportId', 'masterId'])

config = configparser.ConfigParser()
config.read('bot.config')

hooks_conf = Hooks_conf(config['hooks']['sonarPath'],
                        config['hooks']['githubPath'],
                        int(config['hooks']['timeout']))

jenkins_conf = Jenkins_conf(config['jenkins']['token'],
                            config['jenkins']['path'],
                            config['jenkins']['site'],
                            config['jenkins']['project'])

discord_conf = Discord_conf(config['discord']['token'],
                            config['discord']['activateId'],
                            config['discord']['reportId'],
                            config['discord']['masterId'])

print(f"""[INFO] here is the configuration:
[hooks]:
    sonarPath: {hooks_conf.sonarPath}
    githubPath: {hooks_conf.githubPath}
    timeout: {hooks_conf.timeout}

[jenkins]:
    token: {jenkins_conf.token}
    path: {jenkins_conf.path}
    site: {jenkins_conf.site}
    project: {jenkins_conf.project}

[discord]:
    token: {discord_conf.token}
    activateId: {discord_conf.activateId}
    reportId: {discord_conf.reportId}
    masterId: {discord_conf.masterId}
""")
