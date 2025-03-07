# SPDX-FileCopyrightText: 2025 DB Systel GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Main functions of purl-tools"""

import argparse
import logging

from . import __version__
from .purl2cd import purl2clearlydefined
from .repo_api import get_metadata
from .url_purl import convert_purl2url, convert_url2purl

# Main parser with root-level flags
parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
# First-level subcommands
subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

# Common flags, usable for all effective subcommands
common_flags = argparse.ArgumentParser(add_help=False)  # No automatic help to avoid duplication
common_flags.add_argument("-v", "--verbose", action="store_true", help="Verbose output (DEBUG)")

# purl2clearlydefined
parser_purl2cd = subparsers.add_parser(
    "purl2cd",
    help="Convert a PackageURL to ClearlyDefined.io coordinates",
    parents=[common_flags],
)
parser_purl2cd.add_argument("purl", help="The PackageURL to convert")

# url2purl
parser_url2purl = subparsers.add_parser(
    "url2purl",
    help="Convert an URL to a PURL",
    parents=[common_flags],
)
parser_url2purl.add_argument("url", help="The URL to convert")

# purl2url
parser_purl2url = subparsers.add_parser(
    "purl2url",
    help="Convert a PURL to an URL",
    parents=[common_flags],
)
parser_purl2url.add_argument("purl", help="The PURL to convert")

# meta
parser_meta = subparsers.add_parser(
    "meta",
    help="Get metadata for a package by its PURL",
    parents=[common_flags],
)
parser_meta.add_argument("purl", help="The PURL to look up")
parser_meta.add_argument(
    "info", help="The information to look up", choices=["latest", "repository"]
)


def configure_logger(verbose: bool = False) -> logging.Logger:
    """Set logging options"""
    log = logging.getLogger()
    logging.basicConfig(
        encoding="utf-8",
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    return log


def _cli():
    """Main function for CLI."""
    args = parser.parse_args()
    configure_logger(args.verbose)

    if args.command == "purl2cd":
        print(purl2clearlydefined(args.purl))
    elif args.command == "url2purl":
        print(convert_url2purl(args.url))
    elif args.command == "purl2url":
        print(convert_purl2url(args.purl))
    elif args.command == "meta":
        print(get_metadata(args.purl, args.info))


if __name__ == "__main__":
    _cli()
