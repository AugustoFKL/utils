#!/bin/bash

# This script is used exclusively in the CI workflow to extract the Rust channel version
# from the rust-toolchain.toml file and set it as an environment variable for GitHub Actions.

# Safety features
set -euo pipefail # Stop on error, unset variables, and fail on failed pipes.

# Extract the version from rust-toolchain.toml
# Assuming version is in the format "channel = "1.2.3"" in the rust-toolchain.toml file
# Using awk for cleaner parsing instead of double grep.
version=$(awk -F'"' '/channel =/ {print $2}' rust-toolchain.toml)

# Check if the version was successfully extracted
if [ -z "$version" ]; then
    echo "Failed to extract version from rust-toolchain.toml" >&2
    exit 1
fi

# Print the version
echo "version=$version"

# Write the version to the GitHub output
# This sets the GITHUB_OUTPUT environment variable for use in GitHub Actions
echo "version=$version" >>"$GITHUB_OUTPUT"
