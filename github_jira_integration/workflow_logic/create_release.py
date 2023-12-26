import json
import sys

from github_jira_integration.tools.log import logger


def create_release(release):
    """
    Creates a release in Jira with the given information.

    If the release already exists, an error is returned. Updating the
    release should happen with clear intent, so this function does not
    update releases for that reason.

    :param release: The release JSON object from the GitHub event payload. See
                    `GitHub API documentation
                    <https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#get-a-release>`_
                    for more information.
    :return: None
    """

    logger.info("Creating release in Jira...")

    print(json.dumps(release, indent=4))


def main(release):
    """
    Main function to run the script.

    :return: None
    """

    logger.info("Running create_release.py...")

    create_release(release)

    logger.info("create_release.py finished successfully")

    exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python create_release.py <release>")
        exit(1)

    release = json.loads(sys.argv[1])

    main(release)
