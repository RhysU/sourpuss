# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import io
import textwrap

import pandas
import pytest

import sourpuss


def data_basic():
    return pandas.read_csv(io.StringIO(textwrap.dedent("""
        name,city,phone-number,date
        Katherine Rivera,Pavo,540-489-5084,1973-01-18
        Katie Estrada,Antler,992-454-3547,2003-07-07
        Scott Harris,Colesville,665-552-3378,1989-01-01
        Anthony Flores,Round Oak,437-057-2113,1975-01-27
        Deborah Clark,Balcones Heights,871-803-9642,1978-02-07
        Andrea Owens,Lucile,308-267-6029,2018-01-05
        Kimberly Myers,Holly Ridge,906-150-0581,2002-02-26
        Katherine Garner,Dalton City,687-950-3807,1984-06-16
        Brianna Preston,Bernice,489-937-8732,1970-11-28
        Justin Herman,Milleville Beach,847-845-5160,1984-11-10
    """)))


@pytest.mark.parametrize("data", [
    data_basic()
])
def test_coerce(data):
    result = sourpuss.coerce_to_df(data)
    assert isinstance(result, pandas.DataFrame)
