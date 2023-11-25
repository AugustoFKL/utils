import subprocess
import sys

from log import logger


class CommitValidator:
    """
    A class for validating commit messages in a git repository.

    Attributes:
        subprocess_module: A module for running subprocess commands, default to the subprocess module.
    """

    def __init__(self, subprocess_module=subprocess):
        """
        Initializes the CommitValidator with a subprocess module.

        Args:
            subprocess_module: A module for running subprocess commands, default to the subprocess module.
        """
        self.subprocess = subprocess_module

    def get_commit_hashes(self, base_branch):
        """
        Retrieves a list of commit hashes from the specified base branch to HEAD.

        Args:
            base_branch: The base branch to compare with HEAD.

        Returns:
            A list of commit hashes, or an empty list if an error occurs.
        """
        try:
            commit_hashes = (
                self.subprocess.check_output(
                    ["git", "rev-list", "--no-merges", f"{base_branch}..HEAD"],
                    text=True,
                )
                .strip()
                .split("\n")
            )
            return commit_hashes
        except Exception as e:
            logger.error(f"Failed to get commit hashes: {e}")
            return []

    def validate_commit_message(self, commit_hash):
        """
        Validates a single commit message using Commitizen.

        Args:
            commit_hash: The hash of the commit to validate.

        Returns:
            True if the commit message is valid, False otherwise.
        """
        try:
            self.subprocess.check_output(
                ["cz", "check", "--commit-msg-file", commit_hash],
                stderr=self.subprocess.STDOUT,
            )
            logger.info(f"Commit {commit_hash} passed validation.")
            return True
        except Exception as e:
            logger.error(f"Validation failed for commit {commit_hash}: {e}")
            return False

    def validate_commits(self, base_branch):
        """
        Validates all commit messages from the specified base branch to HEAD.

        Args:
            base_branch: The base branch to compare with HEAD.

        Returns:
            True if all commit messages are valid, False otherwise.
        """
        commit_hashes = self.get_commit_hashes(base_branch)
        invalid_commits = [
            commit
            for commit in commit_hashes
            if not self.validate_commit_message(commit)
        ]

        if invalid_commits:
            logger.error("Invalid commit messages found for commits:")
            for commit in invalid_commits:
                logger.error(commit)
            return False
        else:
            logger.info("All commit messages are valid.")
            return True


def main(base_branch):
    """
    Main function to validate commit messages.

    Args:
        base_branch: The base branch to compare with HEAD.
    """
    validator = CommitValidator()
    if not validator.validate_commits(base_branch):
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Error: Base branch argument is missing")
        sys.exit(1)
    main(sys.argv[1])
