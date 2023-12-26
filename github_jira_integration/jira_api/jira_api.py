import jira.resources
from jira import JIRA

from github_jira_integration.tools.log import logger
from github_jira_integration.tools.settings import (
    get_jira_token,
    get_jira_email,
)


class JiraApi:
    domain = "https://augustofotino.atlassian.net"
    jira_client: JIRA

    def __init__(self):
        email = get_jira_email()
        token = get_jira_token()

        self.jira_client = JIRA(server=self.domain, basic_auth=(email, token))

    def get_issue(self, issue_id):
        """
        Gets the issue from Jira.

        :param issue_id: The identifier (for example, "SQLC-123") for the
                         issue.

        :return: The issue from Jira.
        """

        logger.info(f"Getting issue {issue_id}...")
        issue = self.jira_client.issue(issue_id)
        logger.debug(f"...issue found successfully")

        return issue

    # TODO(future): Add support for description, release date, and start date
    # TODO(<create-issue>): Add support for archived and released.
    def create_release(self, name, project_key):
        """
        Creates a release in Jira with the given information.

        If the release already exists, an error is returned.
        Updating the release should happen with clear intent, so this function
        does not update releases for that reason.

        :param name: The name of the release.
        :param project_key: The project for the release.

        :return: None
        """

        logger.info(f"Creating release {name}...")
        self.jira_client.create_version(name, project_key)
        logger.debug(f"...release created successfully")

    def delete_release(self, name, project_key):
        """
        Deletes the release with the given name.

        :param name: The name of the release.
        :param project_key: The project for the release.

        :return: None
        """

        logger.info(f"Deleting release {name}...")
        release: jira.resources.Version = self.get_release_by_name(
            name, project_key
        )
        release.delete()
        logger.debug(f"...release deleted successfully")

    def get_release_by_name(self, name, project):
        """
        Gets the release by name.

        :param name: The name of the release.
        :param project: The project for the release.

        :return: The release by name or None if it doesn't exist.
        """

        logger.info(f"Getting release by name {name}...")
        release = self.jira_client.get_project_version_by_name(project, name)
        logger.debug(f"...release found successfully")

        return release
