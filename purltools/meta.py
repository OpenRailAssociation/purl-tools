# SPDX-FileCopyrightText: 2025 DB Systel GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Functions to query package repository APIs in order to get package metadata like versions and
code URLs"""

import logging
from urllib.parse import quote

import requests
from packageurl import PackageURL


def _handle_none_namespace(namespace: str | None) -> str:
    """Handle the case where the namespace is None."""
    if namespace is None:
        return ""
    return namespace


def _api_query(url):
    """Make a generic GET request with some error handling. Returns the JSON response."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


def query_depsdev_for_metadata(system: str, namespace: str | None, name: str, info: str):
    """Query the deps.dev API in two steps:
    1. Get latest version: https://api.deps.dev/v3/systems/:repo/packages/:name
    2. Get metadata for this version:
       https://api.deps.dev/v3/systems/:repo/packages/:name/versions/:latest
    """
    namespace = _handle_none_namespace(namespace)
    if system == "maven":
        # For Maven, the package name is in the form of "group:artifact"
        package = quote(f"{namespace}:{name}" if namespace else name, safe="")
    else:
        package = quote(f"{namespace}/{name}" if namespace else name, safe="")

    url = f"https://api.deps.dev/v3/systems/{system}/packages/{package}"
    data: dict = _api_query(url)

    latest_version = [
        version["versionKey"]["version"] for version in data["versions"] if version["isDefault"]
    ][0]

    if info == "latest":
        return latest_version
    if info == "repository":
        url = f"{url}/versions/{latest_version}"
        data_version: dict = _api_query(url)
        links = data_version.get("links", [])
        source_url = next((link["url"] for link in links if link["label"] == "SOURCE_REPO"), "")

        # Return source URL after removing potential git+ prefix and .git suffix (e.g. in npm)
        return source_url.removeprefix("git+").removesuffix(".git")

    raise ValueError("Invalid info type")


def get_metadata_packagist(namespace: str | None, name: str, info: str) -> str:
    """Query the packagist (composer) registry API to get metadata about a package.

    Args:
        namespace (str | None): The namespace of the package. Can be empty or None.
        name (str): The name of the package.
        info (str): The type of information to query. One of "latest" or "repository".

    Returns:
        str: The requested information.
    """
    # Example: https://repo.packagist.org/p2/symfony/polyfill-mbstring.json

    namespace = _handle_none_namespace(namespace)

    url = f"https://repo.packagist.org/p2/{namespace}/{name}.json"
    data: dict = _api_query(url)

    data_pkg = data.get("packages", {}).get(f"{namespace}/{name}", [{}])[0]
    if info == "latest":
        return data_pkg.get("version", "")
    if info == "repository":
        return data_pkg.get("source", {}).get("url", "").replace(".git", "")

    raise ValueError("Invalid info type")


def get_metadata(purl: str, info: str) -> str:
    """Get metadata about a package from a repository API."""
    try:
        p = PackageURL.from_string(purl)
        logging.debug("Deconstructed Package URL: %s", repr(p))
    except ValueError as e:
        raise ValueError(f"Failed to parse purl: {e}") from e

    if info not in ["latest", "repository"]:
        raise ValueError("Invalid info type")

    # For many package types, we use the deps.dev API to simplify maintenance
    if p.type in ("npm", "pypi", "cargo", "maven", "golang", "nuget"):
        # "golang" in PURL is "go" in deps.dev
        if p.type == "golang":
            repo_system = "go"
        else:
            repo_system = p.type

        return query_depsdev_for_metadata(
            system=repo_system, namespace=p.namespace, name=p.name, info=info
        )
    # For other package types, we query the respective registry APIs
    if p.type == "composer":
        return get_metadata_packagist(namespace=p.namespace, name=p.name, info=info)

    raise ValueError(f"Unsupported package type: {p.type}")
