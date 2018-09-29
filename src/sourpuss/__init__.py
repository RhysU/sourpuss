#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Cat Python pickle file(s) onto standard output, especially DataFrames."""
import operator
import os
import sys
import typing

import click
import pandas

# TODO Handle non-DataFrame pickles
# TODO Permit sorting all rows


# What types of paths can we hope to load successfully?
PicklePath = click.Path(exists=True, file_okay=True, dir_okay=False,
                        writable=False, readable=True, resolve_path=False,
                        allow_dash=False, path_type=None)

# What defaults are selected for configurable display parameters?
DEFAULT_PRECISION = 17


@click.command()
@click.argument('file', nargs=-1, type=PicklePath)
@click.option('--csv', '-c', is_flag=True,
              help='Emit CSV instead of formatted table.')
@click.option('--no-index', '-n', is_flag=True,
              help='Do not display the index.')
@click.option('--location', '-l', is_flag=True,
              help='Prefix each row with the location of the file')
@click.option('--multi-sparse', '-s', is_flag=True,
              help='Sparsify any MultiIndex display.')
@click.option('--precision', '-p', type=click.IntRange(min=1, max=None),
              show_default=True, metavar='DIGITS', default=DEFAULT_PRECISION,
              help='Change precision for floating point.')
@click.option('--query', '-q', type=str, metavar='QUERY',
              help='Show only rows satisfying a query.')
@click.option('--sort', '-s', is_flag=True,
              help='Sort according to the index.')
@click.option('--types', '-t', is_flag=True,
              help='Show the type, not the value, of each datum.')
def main(
        file: typing.List[str],
        *,
        csv: typing.Optional[bool] = None,
        no_index: typing.Optional[bool] = None,
        location: typing.Optional[bool] = None,
        multi_sparse: typing.Optional[bool] = None,
        precision: typing.Optional[int] = None,
        query: typing.Optional[str] = None,
        sort: typing.Optional[bool] = None,
        types: typing.Optional[bool] = None
):
    """Cat Python pickle file(s) onto standard output, especially DataFrames."""
    with kid_gloves_off(multi_sparse=multi_sparse, precision=precision):
        for f in file:
            # Load and transform the file
            df = pandas.read_pickle(f)
            if isinstance(df, pandas.Series):
                df = df.to_frame()
            if location:
                df.insert(loc=0, column='location', value=f)
            if query is not None:
                df = df.query(query)
            if types:
                df = (df.applymap(type)
                      .applymap(operator.attrgetter('__name__')))
            if sort:
                df = df.sort_index(axis=0, kind='mergesort')

            # Emit output in the desired format
            if csv:
                df.to_csv(sys.stdout, index=not no_index)
            else:
                df.to_string(sys.stdout, index=not no_index)
                if not df.empty:
                    sys.stdout.write(os.linesep)


def kid_gloves_off(
        multi_sparse: typing.Optional[bool] = None,
        precision: typing.Optional[int] = None,
) -> pandas.option_context:
    """Like, seriously, Pandas just give me the entirety of my data."""
    return pandas.option_context(
        'display.date_yearfirst', True,
        'display.expand_frame_repr', True,
        'display.max_categories', 1024,
        'display.max_columns', None,
        'display.max_colwidth', 1024,
        'display.max_rows', None,
        'display.max_seq_items', None,
        'display.multi_sparse', bool(multi_sparse),
        'display.precision', (precision if precision is not None
                              else DEFAULT_PRECISION),
        'display.show_dimensions', False,
        'display.width', None,
    )


if __name__ == '__main__':
    main()
