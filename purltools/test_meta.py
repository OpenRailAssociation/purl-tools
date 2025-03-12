# SPDX-FileCopyrightText: 2025 DB Systel GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Test meta functions"""

from pytest import raises

from purltools.meta import (
    _handle_none_namespace,
    get_metadata,
    query_depsdev_for_metadata,
)


def test_handle_none_namespace_with_none():
    """
    Test _handle_none_namespace() with a None namespace input.
    """
    assert _handle_none_namespace(None) == ""


def test_handle_none_namespace_with_empty_string():
    """
    Test _handle_none_namespace() with an empty string namespace input.
    """
    assert _handle_none_namespace("") == ""


def test_handle_none_namespace_with_namespace():
    """
    Test _handle_none_namespace() with a non-None namespace input.
    """
    assert _handle_none_namespace("example_namespace") == "example_namespace"


def test_query_depsdev_for_metadata_pypi():
    """
    Test query_depsdev_for_metadata() with a valid input and predictable output.
    """
    system = "pypi"
    namespace = None
    name = "tlscanary"

    latest = query_depsdev_for_metadata(
        system=system, namespace=namespace, name=name, info="latest"
    )
    repository = query_depsdev_for_metadata(
        system=system, namespace=namespace, name=name, info="repository"
    )

    assert latest == "4.0.2"
    assert repository == "https://github.com/mozilla/tls-canary"


def test_get_metadata_unsupported():
    """
    Test get_metadata() with an unsupported system.
    """
    with raises(ValueError):
        unsupported_purl = "pkg:cocoapods/AFNetworking@4.0.1"
        get_metadata(purl=unsupported_purl, info="latest")


def test_get_metadata_pypi():
    """
    Test get_metadata() with PyPI as system.
    """
    pypi_purl = "pkg:pypi/tlscanary"
    latest = get_metadata(purl=pypi_purl, info="latest")
    repository = get_metadata(purl=pypi_purl, info="repository")

    assert latest == "4.0.2"
    assert repository == "https://github.com/mozilla/tls-canary"


def test_get_metadata_pypi_version():
    """
    Test get_metadata() with PyPI as system, using a purl with version.
    """
    pypi_purl = "pkg:pypi/tlscanary@42.23"
    latest = get_metadata(purl=pypi_purl, info="latest")
    repository = get_metadata(purl=pypi_purl, info="repository")

    assert latest == "4.0.2"
    assert repository == "https://github.com/mozilla/tls-canary"
