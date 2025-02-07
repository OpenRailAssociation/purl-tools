"""Test purl2clearlydefined()"""

from pytest import raises

from purltools import purl2clearlydefined


def test_purl2cd_empty_version(caplog):
    """App shall fail when no version in purl given"""
    purl = "pkg:cocoapods/AFNetworking"
    with raises(SystemExit):
        purl2clearlydefined(purl)
        assert "Version is None. This is required" in caplog


def test_purl2cd_empty_version_with_quali(caplog):
    """App shall fail when no version in purl given, even if qualifier given"""
    purl = "pkg:deb/debian/mini-httpd@?arch=arm64&distro=buster"
    with raises(SystemExit):
        purl2clearlydefined(purl)
        assert "Version is None. This is required" in caplog


def test_purl2cd_cocoapods():
    """CocoaPods packages"""
    purl = "pkg:cocoapods/AFNetworking@4.0.1"
    expected_coordinates = "pod/cocoapods/-/AFNetworking/4.0.1"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_cargo():
    """cargo (crates.io) packages"""
    purl = "pkg:cargo/bitflags@1.0.4"
    expected_coordinates = "crate/cratesio/-/bitflags/1.0.4"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_composer():
    """Composer (PHP) packages"""
    purl = "pkg:composer/symfony/polyfill-mbstring@v1.11.0"
    expected_coordinates = "composer/packagist/symfony/polyfill-mbstring/v1.11.0"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_conda():
    """Conda packages"""
    purl = "pkg:conda/absl-py@0.4.1?build=py36h06a4308_0&channel=main&subdir=linux-64&type=tar.bz2"
    expected_coordinates = "conda/anaconda-main/linux-64/absl-py/0.4.1-py36h06a4308_0"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_deb():
    """Debian packages"""
    purl = "pkg:deb/debian/mini-httpd@1.30-0.2?arch=arm64&distro=buster"
    expected_coordinates = "deb/debian/-/mini-httpd/1.30-0.2_arm64"

    assert purl2clearlydefined(purl) == expected_coordinates

    purl = "pkg:deb/debian/mini-httpd@1.30-0.2?arch=source"
    expected_coordinates = "debsrc/debian/-/mini-httpd/1.30-0.2"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_gem():
    """Gem (Ruby) packages"""
    purl = "pkg:gem/sorbet@0.5.11798"
    expected_coordinates = "gem/rubygems/-/sorbet/0.5.11798"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_github_commit():
    """GitHub PURLs using commit"""
    purl = (
        "pkg:github/openrailassociation/github-org-manager@cecadcd39d4d741daa21551beb8f2855cf6b1dc6"
    )
    expected_coordinates = (
        "git/github/openrailassociation/github-org-manager/cecadcd39d4d741daa21551beb8f2855cf6b1dc6"
    )

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_github_tag():
    """GitHub PURLs using a tag"""
    purl = "pkg:github/openrailassociation/github-org-manager@v0.5.7"
    expected_coordinates = (
        "git/github/openrailassociation/github-org-manager/1004ad1ac52465b97602a93d25d3ea1713d4b5d8"
    )

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_pypi():
    """PyPI packages"""
    purl = "pkg:pypi/backports.ssl-match-hostname@3.7.0.1"
    expected_coordinates = "pypi/pypi/-/backports.ssl-match-hostname/3.7.0.1"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_npm_normal():
    """NPM packages without group"""
    purl = "pkg:npm/ansi-styles@6.2.1"
    expected_coordinates = "npm/npmjs/-/ansi-styles/6.2.1"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_npm_group():
    """NPM packages with group"""
    purl = "pkg:npm/@vitest/utils@3.0.5"
    expected_coordinates = "npm/npmjs/@vitest/utils/3.0.5"

    assert purl2clearlydefined(purl) == expected_coordinates


def test_purl2cd_npm_group_url_encoded():
    """NPM packages with group, @ URL-encoded"""
    purl = "pkg:npm/%40vitest/utils@3.0.5"
    expected_coordinates = "npm/npmjs/@vitest/utils/3.0.5"

    assert purl2clearlydefined(purl) == expected_coordinates
