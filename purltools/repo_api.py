# SPDX-FileCopyrightText: 2025 DB Systel GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Functions to query package repository APIs in order to get package metadata like versions and
code URLs"""

import logging

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


def get_metadata_crates(name: str, info: str) -> str:
    """Query the crates.io (cargo) registry API to get metadata about a package.

    Args:
        name (str): The name of the package.
        info (str): The type of information to query. One of "latest" or "repository".

    Returns:
        str: The requested information.
    """
    # Example: https://crates.io/api/v1/crates/bitflags

    url = f"https://crates.io/api/v1/crates/{name}"
    data: dict = _api_query(url)

    if info == "latest":
        return data.get("crate", {}).get("default_version", "")
    if info == "repository":
        return data.get("crate", {}).get("repository", "")

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


def get_metadata_npm(namespace: str | None, name: str, info: str) -> str:
    """Query the npm registry API to get metadata about a package.

    Args:
        namespace (str | None): The namespace of the package. Can be empty or None.
        name (str): The name of the package.
        info (str): The type of information to query. One of "latest" or "repository".

    Returns:
        str: The requested information.
    """
    # Example: https://registry.npmjs.org/@db-ui/v-elements/latest

    namespace = _handle_none_namespace(namespace)

    url = f"https://registry.npmjs.org/{namespace}/{name}/latest"
    data: dict = _api_query(url)

    if info == "latest":
        return data.get("version", "")
    if info == "repository":
        return data.get("repository", {}).get("url", "").replace("git+", "").replace(".git", "")

    raise ValueError("Invalid info type")


def get_metadata_pypi(name: str, info: str) -> str:
    """Query the PyPI registry API to get metadata about a package.

    Args:
        name (str): The name of the package.
        info (str): The type of information to query. One of "latest" or "repository".

    Returns:
        str: The requested information.
    """
    # Example: https://pypi.org/pypi/charset-normalizer/json

    url = f"https://pypi.org/pypi/{name}/json"
    data: dict = _api_query(url)

    if info == "latest":
        return data.get("info", {}).get("version", "")
    if info == "repository":
        # Can be either .Code or .Source
        if repo := data.get("info", {}).get("project_urls", {}).get("Code", ""):
            return repo
        return data.get("info", {}).get("project_urls", {}).get("Source", "")

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

    if p.type == "npm":
        return get_metadata_npm(namespace=p.namespace, name=p.name, info=info)
    if p.type == "pypi":
        return get_metadata_pypi(name=p.name, info=info)
    if p.type == "cargo":
        return get_metadata_crates(name=p.name, info=info)
    if p.type == "composer":
        return get_metadata_packagist(namespace=p.namespace, name=p.name, info=info)

    raise ValueError(f"Unsupported package type: {p.type}")
