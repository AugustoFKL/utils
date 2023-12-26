import json
import subprocess
import sys

from log import logger

# GitHub User/Organization - Replace with your own.
user = "AugustoFKL"


def remove_label(repo, name):
    """
    Remove a label from a GitHub repository.

    Args:
        repo (str): Repository name to remove the label from.
        name (str): Name of the label.
    """

    # Command to remove label using GitHub CLI
    command = (
        f"gh api "
        f"--method DELETE "
        f'-H "Accept: application/vnd.github+json" '
        f'repos/{user}/{repo}/labels/"{name}"'
    )
    try:
        subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.debug(f"Label '{name}' removed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to remove label '{name}': {e.stdout}, {e.stderr}"
        )
        sys.exit(1)


def get_labels(repo):
    """
    Get all labels from a GitHub repository.

    Args:
        repo (str): Repository name to get labels from.

    Returns:
        list: List of labels.
    """

    logger.info(f"Retrieving labels from '{repo}'...")

    command = (
        f"gh api "
        f"--method GET "
        f'-H "Accept: application/vnd.github.v3+json" '
        f"repos/{user}/{repo}/labels"
    )

    try:
        result = subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.debug(f"Labels retrieved successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to retrieve labels: {e.stdout}")
        sys.exit(1)

    response = json.loads(result.stdout.decode("utf-8"))

    labels = []
    for item in response:
        name = item["name"]
        labels.append(name)
        logger.debug(f"Label '{name}' retrieved successfully.")

    return labels


def main(repo):
    """
    Main function to remove all labels from a repository.

    Args:
        repo (str): Repository name to remove labels from.
    """

    labels = get_labels(repo)

    for label in labels:
        remove_label(repo, label)


if __name__ == "__main__":
    logger.info("Starting label setup...")

    # Check if repository name was provided
    if len(sys.argv) == 1:
        logger.error("Repository name isn't provided.")
        sys.exit(1)
    elif len(sys.argv) > 2:
        logger.error(
            "Too many arguments provided expected 1, received {}.".format(
                sys.argv
            )
        )
        sys.exit(1)

    main(sys.argv[1])
