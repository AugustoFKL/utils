import argparse
import os
import re
from pathlib import Path

from log import logger


def set_github_output(variable_name: str, value: str) -> None:
    """
    Sets a GitHub Actions output variable if running in the GitHub Actions environment.
    """
    logger.info(f"Setting output variable '{variable_name}' to '{value}'...")

    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{variable_name}={value}\n")
        logger.debug(f"...output variable set successfully.")
    else:
        logger.warning("...not running on CI, skipping output variable set.")


def get_project_root() -> Path:
    """
    Returns the root directory of the project.

    **Note**: Do not move this file, as it will break the path resolution.
    """

    return Path(__file__).parent.parent


def extract_rust_version(args) -> str:
    """
    Extracts the Rust toolchain version from the given toolchain file.

    If running in a GitHub Actions environment, sets a variable called `version` with the extracted value as an output
    variable.
    """
    logger.info(f"Extracting Rust version...")

    version_pattern = re.compile(r'channel = "([0-9.]+)"')
    try:
        content = Path(args.toolchain_file).read_text()
        version = version_pattern.search(content).group(1)

        logger.debug(f"...{version}...")
        set_github_output("version", version)

        logger.debug(f"...Rust version extracted successfully.")
        return version
    except Exception as e:
        logger.error(f"...error extracting Rust channel: {e}")
        exit(1)


def configure_extract_rust_channel_subcommand(subparsers) -> None:
    """Configures the 'extract-rust-channel' subcommand."""
    parser_extract = subparsers.add_parser(
        "extract-rust-channel", help="Extract Rust channel from toolchain file"
    )
    parser_extract.add_argument(
        "toolchain_file",
        nargs="?",
        default=os.path.join(get_project_root(), "rust-toolchain.toml"),
        help='Path to the rust-toolchain.toml file. Defaults to "rust-toolchain.toml"',
    )
    parser_extract.set_defaults(func=extract_rust_version)


def main():
    parser = argparse.ArgumentParser(
        description="Utility functions for GitHub Actions."
    )
    subparsers = parser.add_subparsers(help="Sub-command help")

    # Each subcommand configuration is encapsulated in its own function
    configure_extract_rust_channel_subcommand(subparsers)

    # Parse the arguments to the appropriate function
    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
