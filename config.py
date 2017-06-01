"""Reads the configuaration file for initialisation constants

The configuration file is bot.config, it follows the classical Windows INI
file format. It has the following sections:

[global]:
Settings that apply to the whole application
    site: The website hosting the ci structure

[hooks]:
The webhooks paths to listen to, for the bottle server
    sonarPath: The path that sonar will request when activating a webhook
    githubPath: The path that github will request when activating a webhook
    timeout/int: How long (in seconds) should the bot wait the sonar report
        until it assumes it simply wont ever answer.

[jenkins]:
Jenkins ci related settings
    token: The token to use to authenticate for jenkins
    tokenPath: the path to use to trigger the build of the project
    path: The base URL for jenkins.
    project: The project that must be built
    cibranch: the branch that jenkins uses to continuously integrate.

[sonar]:
The sonar specific settings
    prefix: the path prefix to the sonar instance.

[discord]:
The discord related settings
    token: The discord token key, to use the bot account.
    activateId: The channel where we recieve commands from.
    reportId: the channel in which to post reports.
    masterId: The user with extra privileges.
    trigger: The message that triggers the Jenkins ci job.
"""
import re
import configparser
from collections import namedtuple

def get_typed_list(options):
    """Returns a tuple of two lists, the option names and the option
    types.

    options: a list of raw config section options, with its possible type
        left in.

    returns: two lists, one of the option names, one of the option types,
        ordered according to the input list."""
    options_names = [x.split('/')[0] for x in options]
    options_types = []
    for option in options:
        try:
            options_types += [option.split('/')[1]]
        except IndexError:
            options_types += ['']
    return options_names, options_types


def docstring_parser():
    """Creates the configuaration specification based on the docstring.

    The docstring explains the content and documents the content of the
    config file, so why not directly use it to dynamically create
    the configs?

    The format is as following:
        Sections are specified with a signle line the following way:

        [<section_name>]:

        where section_name is a valid python identifier the first character
        must NOT be a uppercase letter.

        Options are specified with EXACTLY FOUR LEADING SPACES, the option
        name, and a colon. Every character after the colon is ignored.
        An optional type specification is supported, string types are implicit,
        explicitely declaring them will lead to an error.

            <option_name>[/type]: ....

        All lines that are formatted differently will be ignored, use those
        to explain what the options do."""
    docstring = __doc__
    sections = {}
    current_section = None
    config = configparser.ConfigParser()
    config.read('bot.config')
    for line in docstring.split('\n'):
        match = re.match(r'^\[(\w+)\]:$', line)
        if match is not None:
            current_section = match.group(1)
            if current_section in sections:
                raise configparser.DuplicateSectionError(current_section)
            sections[current_section] = []
            continue

        match = re.match(r'^    (\w+/?\w*):.*$', line)
        if match is not None:
            current_option = match.group(1)
            current_option_list = sections[current_section]
            if current_option in current_option_list:
                raise configparser.DuplicateOptionError(current_section,
                                                        current_option)
            current_option_list += [current_option]

    for section, options in sections.items():
        section_type_name = section.capitalize() + '_conf'
        options_names, options_types = get_typed_list(options)
        globals()[section_type_name] = \
                namedtuple(section_type_name, options_names)
        globals()[section + '_conf'] = globals()[section_type_name] \
            ._make([getattr(config[section], 'get'+options_types[i])(x)
                    for i, x in enumerate(options_names)])

docstring_parser()

print(f"""[INFO] here is the configuration:
[hooks]:
    sonarPath: {hooks_conf.sonarPath}
    githubPath: {hooks_conf.githubPath}
    timeout: {hooks_conf.timeout * 10 // 10}

[jenkins]:
    token: {jenkins_conf.token}
    tokenPath: {jenkins_conf.tokenPath}
    path: {jenkins_conf.path}
    project: {jenkins_conf.project}
    cibranch: {jenkins_conf.cibranch}

[discord]:
    token: {discord_conf.token}
    activateId: {discord_conf.activateId}
    reportId: {discord_conf.reportId}
    masterId: {discord_conf.masterId}
    trigger: {discord_conf.trigger}

[global]:
    site: {global_conf.site}

[sonar]:
    prefix: {sonar_conf.prefix}
""")
