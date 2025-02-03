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


def github_tag_to_commit(owner: str, repo: str, tag: str) -> str:
    """Convert a GitHub tag to a commit hash.

    Args:
        tag (str): The GitHub tag.

    Returns:
        str: The commit hash corresponding to the tag.
    """
    return get_tag_commit_sha(owner, repo, tag)


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


def get_tag_commit_sha(owner: str, repo: str, tag: str) -> str:
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
    token = get_github_token()
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/tags/{tag}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
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
