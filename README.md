<!--
SPDX-FileCopyrightText: 2025 DB Systel GmbH

SPDX-License-Identifier: Apache-2.0
-->

# purl-tools - Helpful PackageURL functions

[![Test suites](https://github.com/OpenRailAssociation/purl-tools/actions/workflows/test.yaml/badge.svg)](https://github.com/OpenRailAssociation/purl-tools/actions/workflows/test.yaml)
[![REUSE status](https://api.reuse.software/badge/github.com/OpenRailAssociation/purl-tools)](https://api.reuse.software/info/github.com/OpenRailAssociation/purl-tools)
[![The latest version of Compliance Assistant can be found on PyPI.](https://img.shields.io/pypi/v/purl-tools.svg)](https://pypi.org/project/purl-tools/)
[![Information on what versions of Python Compliance Assistant supports can be found on PyPI.](https://img.shields.io/pypi/pyversions/purl-tools.svg)](https://pypi.org/project/purl-tools/)

This library serves as a helper for various tasks around Package URL (purl).

## Features

* Convert a PURL to [ClearlyDefined](https://clearlydefined.io) coordinates
* Convert a PURL to a URL (using [packageurl-python](https://github.com/package-url/packageurl-python))
* Convert a URL to a PURL (using [packageurl-python](https://github.com/package-url/packageurl-python))

## Requirements

- Python 3.10+
- Internet connection for accessing the GitHub API, if a human-readable tag is requested

## Installation

### Install and run via pipx (Recommended)

[pipx](https://pypa.github.io/pipx/) makes installing and running Python programs easier and avoids conflicts with other packages. Install it with

```sh
pip3 install pipx
```

The following one-liner both installs and runs this program from [PyPI](https://pypi.org/project/purl-tools/):

```sh
pipx run purl-tools
```

If you want to be able to use purl-tools without prepending it with `pipx run` every time, install it globally like so:

```sh
pipx install purl-tools
```

purl-tools will then be available in `~/.local/bin`, which must be added to your `$PATH`.

After this, make sure that `~/.local/bin` is in your `$PATH`. On Windows, the required path for your environment may look like `%USERPROFILE%\AppData\Roaming\Python\Python310\Scripts`, depending on the Python version you have installed.

To upgrade purl-tools to the newest available version, run this command:

```sh
pipx upgrade purl-tools
```


### Other installation methods

You may also use pure `pip` or `poetry` to install this package.


## CLI Usage

purl-tools provides multiple commands to facilitate different tasks. Each command is invoked through the `purl-tools` command-line interface with specific options.

Depending on your exact installation method, this may be one of

```sh
# Run via pipx
pipx run purl-tools
# Installation via pipx or pip
purl-tools
# Run via poetry
poetry run purl-tools
```

In the following, we will just use `purl-tools`.

### Command Structure

```bash
purl-tools <command> [subcommand-options]
```

### Commands

Please run `purl-tools --help` to get an overview of the commands and global options.

For each command, you can get detailed options, e.g., `purl-tools purl2cd --help`.


## Development and Contribution

We welcome contributions to improve this library. Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for all information.


## License

The content of this repository is licensed under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0).

There may be components under different, but compatible licenses or from different copyright holders. The project is REUSE compliant which makes these portions transparent. You will find all used licenses in the [LICENSES](./LICENSES/) directory.

The project has been started by the [OpenRail Association](https://openrailassociation.org). You are welcome to [contribute](./CONTRIBUTING.md)!
