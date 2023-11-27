import subprocess
import sys

from log import logger


class CommitValidator:
    """
    A class for validating commit messages in a git project.

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

    def validate_commits(self, start_commit, end_commit):
        """
        Validates all commit messages between the start and end commits.

        Args:
            start_commit: The first commit to validate.
            end_commit: The last commit to validate.

        Returns:
            True if all commit messages are valid, False otherwise.
        """
        try:
            self.subprocess.check_output(
                ["cz", "check", "--rev-range", f"{start_commit}..{end_commit}"],
                stderr=self.subprocess.STDOUT,
            )
            logger.info("All commit messages are valid.")
            return True
        except Exception as e:
            logger.debug(f"Input message: {e.args}")

            if isinstance(e, self.subprocess.CalledProcessError):
                logger.error(f"Validation failed with exit code {e.returncode}, error: {e.output}")
            else:
                logger.error(f"Validation failed with unknown error: {e}")
            return False


def main(first_commit, last_commit):
    """
    Main function to validate all commit messages between two commits.

    Args:
        first_commit: The first commit to validate.
        last_commit: The last commit to validate.
    """
    validator = CommitValidator()
    if not validator.validate_commits(first_commit, last_commit):
        sys.exit(1)
