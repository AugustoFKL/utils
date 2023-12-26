from decouple import config

from github_jira_integration.tools.log import logger


def get_config_value(key):
    """
    Gets the value for the given key from the configuration.

    :param key: The key to get the value for.
    :return: The value for the given key.
    """

    logger.info(f"Getting {key}...")

    try:
        value = config(key)
        logger.debug(f"...{key} found successfully")
        return value
    except KeyError:
        logger.error(f"{key} not found")
        exit(1)


def get_jira_email():
    return get_config_value("JIRA_EMAIL")


def get_jira_token():
    return get_config_value("JIRA_TOKEN")


def get_github_token():
    return get_config_value("GITHUB_TOKEN")
