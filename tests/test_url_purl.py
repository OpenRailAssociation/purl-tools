"""Test url2purl and purl2url"""

from purltools import convert_purl2url, convert_url2purl


def test_purl2url():
    """Test purl2url conversion"""
    purl = "pkg:composer/symfony/polyfill-mbstring@v1.11.0"
    expected_url = "https://packagist.org/packages/symfony/polyfill-mbstring#v1.11.0"

    assert convert_purl2url(purl) == expected_url

def test_url2purl():
    """Test url2purl conversion"""
    url = "http://pypi.org/project/github-org-manager/0.5.6/"
    expected_purl = "pkg:pypi/github-org-manager@0.5.6"

    assert convert_url2purl(url) == expected_purl
