Unique characters package
=========================
Unique characters package provides find_unique_characters function
that takes one string argument and returns list of it's unique chars.

Usage looks like this::

    $ python

    >>> from unique_characters.util import find_unique_characters
    >>> find_unique_characters("abcdfff")
    ['a', 'b', 'c', 'd']
    >>> find_unique_characters("aaa")
    []

Also this package has command line interface, wich provides 2 optional arguments:

* --file *FILENAME*
* --string *STRING*

You can pass a string to the script via --string argument, or a path to a text file
via --file argument. Note, --file has higher priority

Typical CLI usage loks like this::

    $ python -m unique_characters --string abcc
    "abcc" => 2
    a, b are present once.

    $ unique_chars --string axx
    "aax" => 1
    x is present once.

