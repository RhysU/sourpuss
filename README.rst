Sourpuss: Like feeding pickles to a cat(1)
==========================================

Sourpuss displays the contents of one or more Python pickle files on
standard output.  Currently, this small utility targets pickled Pandas
DataFrames and supports transforming them in simple ways.  By making it
easy to answer simple questions via Unix pipelines, sourpuss lets you
avoid constantly context switching between $SHELL and Jupyter/IPython.

Help::

    Usage: sourpuss [OPTIONS] [FILE]...

      Cat Python pickle file(s) onto standard output, especially DataFrames.

    Options:
      -a, --append-index TEXT  Append named column to the index.
      -c, --csv                Emit CSV instead of formatted table.
      -l, --location           Prefix each row with the location of the file
      -m, --multi-sparse       Sparsify any MultiIndex display.
      -n, --no-index           Do not display the index.
      -p, --precision DIGITS   Change precision for floating point.  [default: 17]
      -q, --query QUERY        Show only rows satisfying a query.
      -r, --reset-index TEXT   Remove named column from the index.
      -s, --sort-index         Sort according to the index.
      -t, --types              Show the type, not the value, of each datum.
      --help                   Show this message and exit.


Examples::

    $ sourpuss ~/foo.pkl
                   name              city  phone-number        date
    0  Katherine Rivera              Pavo  540-489-5084  1973-01-18
    1     Katie Estrada            Antler  992-454-3547  2003-07-07
    2      Scott Harris        Colesville  665-552-3378  1989-01-01
    3    Anthony Flores         Round Oak  437-057-2113  1975-01-27
    4     Deborah Clark  Balcones Heights  871-803-9642  1978-02-07
    5      Andrea Owens            Lucile  308-267-6029  2018-01-05
    6    Kimberly Myers       Holly Ridge  906-150-0581  2002-02-26
    7  Katherine Garner       Dalton City  687-950-3807  1984-06-16
    8   Brianna Preston           Bernice  489-937-8732  1970-11-28
    9     Justin Herman  Milleville Beach  847-845-5160  1984-11-10


    $ sourpuss ~/foo.pkl -q 'city == "Pavo"'
                   name  city  phone-number        date
    0  Katherine Rivera  Pavo  540-489-5084  1973-01-18


    $ sourpuss ~/foo.pkl -a city -a name -s | head -5
                                       phone-number        date
    city             name
    Antler           Katie Estrada     992-454-3547  2003-07-07
    Balcones Heights Deborah Clark     871-803-9642  1978-02-07
    Bernice          Brianna Preston   489-937-8732  1970-11-28
