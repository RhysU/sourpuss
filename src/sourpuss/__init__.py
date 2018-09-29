#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import typing

import click
import pandas

# TODO Suppress a trivial range index
# TODO Add a path prefix as an index element
# TODO Accept a directory and recursively dump pickles
# TODO Convert all entries in the DataFrame into types via type(...)


# What types of paths can we hope to load successfully?
PicklePath = click.Path(exists=True, file_okay=True, dir_okay=False,
                        writable=False, readable=True, resolve_path=False,
                        allow_dash=False, path_type=None)

# What defaults are selected for configurable display parameters?
DEFAULT_MULTI_SPARSE = False
DEFAULT_PRECISION = 17


@click.command()
@click.argument('file', nargs=-1, type=PicklePath)
@click.option('--multi_sparse', '-s', type=bool, show_default=True,
              default=DEFAULT_MULTI_SPARSE)
@click.option('--precision', '-p', type=int, show_default=True,
              default=DEFAULT_PRECISION)
def main(file, multi_sparse, precision):
    """Cat Python pickle file(s) onto standard output, especially DataFrames."""
    with kid_gloves_off(multi_sparse=multi_sparse, precision=precision):
        for f in file:
            print(f)


def kid_gloves_off(
        multi_sparse: typing.Optional[bool] = None,
        precision: typing.Optional[int] = None,
):
    """Like, seriously, Pandas just give me the entirety of my data."""

    return pandas.option_context(
        'display.date_yearfirst', True,
        'display.expand_frame_repr', True,
        'display.max_categories', 1024,
        'display.max_columns', None,
        'display.max_colwidth', 1024,
        'display.max_rows', None,
        'display.max_seq_items', None,
        'display.multi_sparse', (multi_sparse if multi_sparse is not None
                                 else DEFAULT_MULTI_SPARSE),
        'display.precision', (precision if precision is not None
                              else DEFAULT_PRECISION),
        'display.show_dimensions', False,
        'display.width', None,
    )


if __name__ == '__main__':
    main()
