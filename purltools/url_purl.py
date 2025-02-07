# SPDX-FileCopyrightText: 2025 DB Systel GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Convert between PackageURL and URL. Taken more or less unmodifed from
packageurl."""

from packageurl.contrib import purl2url, url2purl


def convert_purl2url(purl: str) -> str:
    """Convert a PackageURL string to an URL.

    Args:
        purl (str): The PackageURL to convert.

    Returns:
        str: The converted URL.
    """
    return purl2url.get_url(purl)


def convert_url2purl(url: str) -> str:
    """Convert an URL to a PackageURL string.

    Args:
        url (str): The URL to convert.

    Returns:
        str: The converted PackageURL.
    """
    return url2purl.get_purl(url).to_string()
