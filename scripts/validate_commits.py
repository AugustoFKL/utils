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

    def validate_commits(self, base_branch, current_ref):
        """
        Validates all commit messages from the specified base branch to the current reference using Commitizen.

        Args:
            base_branch: The base branch to compare with the current reference.
            current_ref: The current reference, typically 'HEAD'.

        Returns:
            True if all commit messages are valid, False otherwise.
        """
        try:
            self.subprocess.check_output(
                ["poetry", "run", "cz", "check", "--rev-range", f"{base_branch}..{current_ref}"],
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


def main(base_branch, ref="HEAD"):
    """
    Main function to validate commit messages.

    Args:
        base_branch: The base branch to compare with the current reference.
        ref: The current reference, default to HEAD.
    """
    validator = CommitValidator()
    if not validator.validate_commits(base_branch, ref):
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Error: Base branch argument is missing")
        sys.exit(1)
    main(sys.argv[1])
