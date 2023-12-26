import random
import subprocess
import sys

from log import logger

# GitHub User/Organization - Replace with your own.
user = "Vaultree"

# Labels to be added
labels = [
    {
        "name": "env: cross-platform",
        "description": "Affects multiple operating systems.",
    },
    {
        "name": "env: linux",
        "description": "Pertaining to Linux-based systems.",
    },
    {
        "name": "env: macos",
        "description": "Exclusively for macOS-related topics.",
    },
    {
        "name": "env: windows",
        "description": "Windows-specific issues or improvements.",
    },
    {
        "name": "type: build",
        "description": "Changes to the code building process.",
    },
    {
        "name": "type: chore",
        "description": "Routine tasks and project maintenance.",
    },
    {
        "name": "type: ci",
        "description": "Adjustments in CI processes and tools.",
    },
    {
        "name": "type: docs",
        "description": "Exclusively for documentation updates.",
    },
    {
        "name": "type: feat",
        "description": "For new functionalities or significant enhancements.",
    },
    {
        "name": "type: fix",
        "description": "Used to correct and address software defects.",
    },
    {
        "name": "type: perf",
        "description": "Enhances efficiency and speed of existing features.",
    },
    {
        "name": "type: refactor",
        "description": "Internal code improvements without behavior change.",
    },
    {
        "name": "type: revert",
        "description": "Undoing previous code changes.",
    },
    {
        "name": "type: style",
        "description": "For non-functional code style improvements.",
    },
    {
        "name": "type: test",
        "description": "Related to adding or improving test cases.",
    },
    {
        "name": "workflow: critical",
        "description": "High-priority, severe impact issues.",
    },
    {
        "name": "workflow: discussion-needed",
        "description": "Requires collective decision-making.",
    },
    {
        "name": "workflow: good-first-issue",
        "description": "Suitable for new contributors.",
    },
    {
        "name": "workflow: help-wanted",
        "description": "Open call for community contributors.",
    },
    {
        "name": "workflow: needs-triage",
        "description": "New, unassessed issues for review.",
    },
    {
        "name": "workflow: up-for-grabs",
        "description": "Ready for immediate work, not urgent.",
    },
]


def add_label(repo, name, description, color):
    """
    Add a label to a GitHub repository.

    Args:
        repo (str): Repository name to add the label to.
        name (str): Name of the label.
        description (str): Description of the label.
        color (str): Color of the label.
    """

    # Command to add label using GitHub CLI
    command = (
        f"gh api "
        f"--method POST "
        f'-H "Accept: application/vnd.github+json" '
        f"repos/{user}/{repo}/labels "
        f'-f name="{name}" '
        f'-f description="{description}" '
        f'-f color="{color}"'
    )
    try:
        subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.debug(f"Label '{name}' added successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to add label '{name}': {e.stdout}")
        sys.exit(1)


# Function to generate a random color
def generate_random_color():
    """
    Generate a random color in hex format, e.g. #FFFFFF.
    """
    return format(random.randint(0, 0xFFFFFF), "06X")


def main(repo):
    """
    Main function.

    Args:
        repo (str): Repository name to setup labels for.
    """

    # Add each label to the repository
    for label in labels:
        add_label(
            repo, label["name"], label["description"], generate_random_color()
        )

    logger.info("All labels added successfully.")


if __name__ == "__main__":
    logger.info("Starting label setup...")

    # Check if repository name was provided
    if len(sys.argv) == 1:
        logger.error("Repository name isn't provided.")
        sys.exit(1)
    elif len(sys.argv) > 2:
        logger.error(
            "Too many arguments provided, expected 1, received {}.".format(
                sys.argv
            )
        )
        sys.exit(1)

    main(sys.argv[1])
