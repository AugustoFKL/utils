import argparse
import json
import subprocess
import sys

from log import logger


def list_caches(repo):
    """List all GitHub Actions caches for a given repository."""
    logger.info(f"Retrieving caches from '{repo}'...")

    arguments = [
        f"gh",
        f"cache",
        f"list",
        f"--repo",
        repo,
        f"--json",
        f"id,key,lastAccessedAt",
    ]

    try:
        result = subprocess.run(
            arguments,
            capture_output=True,
            text=True,
        )
        logger.debug(
            f"...caches retrieved successfully, parsing JSON output from {result}..."
        )
        json_output = json.loads(result.stdout)

    except subprocess.CalledProcessError as e:
        logger.error(f"error listing caches: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"error parsing JSON output: {e}")
        sys.exit(1)

    logger.debug(
        f"...parsed JSON output successfully: {json_output}, returning caches..."
    )

    return json_output


def delete_cache(repo, cache_id):
    """Delete a specific cache by ID for a given repository."""
    result = subprocess.run(
        ["gh", "cache", "delete", cache_id, "--repo", repo, "--confirm"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(f"Error deleting cache {cache_id}: {result.stderr}")
    print(f"Deleted cache {cache_id}")


def main(repo):
    caches = list_caches(repo)
    logger.info(f"Retrieved {len(caches)} caches from '{repo}'.")
    # one_week_ago = datetime.now() - timedelta(days=7)
    #
    # for cache in caches:
    #     last_accessed = datetime.strptime(
    #         cache["last_accessed_at"], "%Y-%m-%dT%H:%M:%SZ"
    #     )
    #     if last_accessed < one_week_ago:
    #         print(
    #             f"Cache {cache['id']} last accessed at {cache['last_accessed_at']} is older than a week."
    #         )
    #         delete_cache(repo, cache["id"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete GitHub Actions caches older than a week for a specified repository."
    )
    parser.add_argument(
        "-r",
        "--repo",
        type=str,
        required=True,
        help='The GitHub repository in the format "owner/repo".',
    )

    args = parser.parse_args()
    main(args.repo)
