# SPDX-FileCopyrightText: 2025 DB Systel GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""GitHub API helper functions"""

import logging
import os

import requests


def is_sha1(sha: str) -> bool:
    """Check if a string is a valid SHA1 hash.

    Args:
        sha (str): The string to check.

    Returns:
        bool: True if the string is a valid SHA1 hash, False otherwise.
    """
    return len(sha) == 40 and all(c in "0123456789abcdef" for c in sha.lower())


def _get_github_tag_info(owner: str, repo: str, tag: str, headers: dict) -> dict:
    """
    Get information about a GitHub tag using GitHub's REST API.
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        tag (str): Tag name/reference
        headers (dict): Headers to include in the API request

    Returns:
        dict: The JSON response from the GitHub API

    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    logging.debug("Resolving GitHub tag %s in repo %s/%s to commit SHA", tag, owner, repo)

    url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/tags/{tag}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def github_tag_to_commit(owner: str, repo: str, tag: str) -> str:
    """Convert a GitHub tag to a commit hash using GitHub's REST API.

    Args:
        owner (str): Repository owner
        repo (str): Repository name
        tag (str): Tag name/reference

    Returns:
        str: The commit SHA the tag points to

    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    # Set Headers for GitHub API request
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = get_github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # First try to get the tag info directly
    try:
        data = _get_github_tag_info(owner, repo, tag, headers)
    # If the tag is not found and does not start with 'v', try again with 'v' prefix. Needed for
    # GitHub actions and cdxgen
    except requests.exceptions.RequestException as e:
        status_code = getattr(e.response, "status_code", None)
        if status_code == 404 and not tag.startswith("v"):
            logging.debug("Tag %s not found, retrying with 'v' prefix", tag)
            try:
                data = _get_github_tag_info(owner, repo, f"v{tag}", headers)
            except requests.exceptions.RequestException:
                if getattr(e.response, "status_code", None) == 404:
                    logging.error("Tag %s (or v%s) not found in repo %s/%s", tag, tag, owner, repo)
                    return tag
                raise e from e
        else:
            raise

    # Tag refs point to annotated tags first, which then point to commits
    if data["object"]["type"] == "tag":
        # Get the commit URL from the annotated tag
        tag_url = data["object"]["url"]
        validate_tag_url(tag_url)
        tag_response = requests.get(tag_url, headers=headers, timeout=10)
        tag_response.raise_for_status()
        return tag_response.json()["object"]["sha"]

    # Lightweight tags point directly to commits
    return data["object"]["sha"]


def validate_tag_url(url: str) -> None:
    """Validate a GitHub API URL to prevent server-side request forgery"""
    if not url.startswith("https://api.github.com"):
        raise ValueError(f"Invalid GitHub API URL '{url}")
    if not is_sha1(url.split("/")[-1]):
        raise ValueError(f"Invalid SHA1 hash in URL '{url}'")


def get_github_token() -> str | None:
    """Get GitHub token from environment variable if available"""
    if "GITHUB_TOKEN" in os.environ and os.environ["GITHUB_TOKEN"]:
        logging.debug("GitHub token found in environment")
        return str(os.environ["GITHUB_TOKEN"])
    logging.debug("No GitHub token found, proceeding unauthenticated")
    return None
