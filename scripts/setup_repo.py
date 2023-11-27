from log import logger

import subprocess
import sys


def install_pre_commit_hooks():
    """Install pre-commit hooks for the repository. Check the pre-commit-config.yaml file for the list of hooks."""

    logger.info("Setting up pre-commit hooks...")
    try:
        subprocess.check_call(["poetry", "run", "pre-commit", "install"])
        logger.debug(f"Successfully set up hooks")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to set up hooks, error: {e.output}")
        sys.exit(1)


def main():
    logger.info("Setting up repository...")

    # Install pre-commit hooks
    install_pre_commit_hooks()

    logger.info("Setup complete.")


if __name__ == "__main__":
    main()
