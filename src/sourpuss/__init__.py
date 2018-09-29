#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import click


@click.command()
@click.argument('file', type=click.File('rb'), nargs=-1)
def main(file):
    """Cat a Python pickle file onto standard output, especially DataFrames."""
    for f in file:
        print(f)


if __name__ == '__main__':
    main()
