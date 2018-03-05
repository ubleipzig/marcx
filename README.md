README
======

`marcx.Record` is a small extension to
[pymarc.Record](https://github.com/edsu/pymarc/blob/056cea129758c20068aec11a4cb148d65987d905/pymarc/record.py#L72),
that adds a few shortcuts: `itervalues`, `test`, `add` and `remove`.

[![Build Status](http://img.shields.io/travis/ubleipzig/marcx.svg?style=flat)](https://travis-ci.org/ubleipzig/marcx)
[![pypi version](http://img.shields.io/pypi/v/marcx.svg?style=flat)](https://pypi.python.org/pypi/marcx)

<!---
[![PyPi version](https://img.shields.io/pypi/v/marcx.svg)](https://crate.io/packages/marcx/)
-->

Since version 0.2.0, both Python 2 and 3 should be supported.

Installation
------------

It's on [pypi](https://pypi.python.org/pypi/marcx), so just:

    $ pip install marcx

Python 2.6 or higher required. If you want to run the tests, too, you'll need 2.7 or higher. Python 3 should work, too.

Overview
--------

Iterate over field values quickly with `itervalues` and `iterfields`:

```python
>>> from urllib import urlopen # from urllib.request import urlopen
>>> import marcx
>>> record = marcx.Record(data=urlopen("http://goo.gl/lfJnw9").read())

>>> record.itervalues('020.a')
<generator object values at 0x2d97690>

>>> set(record.itervalues('020.a'))
set(['020161622X'])
```

A variable number of specs can be passed:

```python
>>> set(record.itervalues('001', '005', '700.a'))
set(['20040816084925.0', 'Thomas, David,', '11778504'])
```

Iterate over fields, but instead of just returning the values, return
tuples of the form `(field, value)`:

```python
>>> for fv in record.iterfields('020.a'): print(fv)
(<pymarc.field.Field object at 0x18e7990>, '020161622X')
```

----

Test a field or subfield with predicates. Pass any function, that returns
a boolean value to `test` and it gets evaluated over all values
(pass `all=True` if *all* values must evaluate to `True` in the test function):

```python
>>> record.test('001', lambda v: sum([int(d) for d in v]) == 33)
True

>>> record.test('020.a', lambda v: v.startswith('978'), all=True)
False
```

----

Test, if a record has any values at all in a certain field or subfield:

```python
>>> record.has('020')
True
>>> record.has('020.a')
True
>>> record.has('020.x')
False
```

----

Add and remove fields with one line (control fields get `data`, non-control
fields get subfields via [keyword
arguments](https://docs.python.org/3/tutorial/controlflow.html#keyword-arguments)):

```python
>>> record = marcx.Record()
>>> record.add('001', data='12345')
>>> record.add('020', a='9780201616224')
>>> record.add('020', a='020161622X')
>>> record.remove('001')
```

Note: *The order of the keyword arguments is not preserved* in Python 3.5 or
earlier. However, Python 3.6 implemented [PEP 468: Preserving Keyword Argument
Order](https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep468) and
therefore subfields actually will be added in the order they are specified.

Add repeated subfields:

```python
>>> record.remove('020.a')
>>> record.add('020', a=['9780201616224', '020161622X'])
```

Add fields with many subfields at once:

```python
>>> record.add('990', a='1', b='2', c='3', d='5', e='6')
```

Add numeric subfield with underscores:

```python
>>> record.add('991', _0='Zero', _1='One', _9='Nine')
```

----

Flatten all values in a MARC record, e.g. to build corpuses:

```python
>>> record = marcx.Record(data=urlopen("http://goo.gl/lfJnw9").read())
>>> record.flatten()
['11778504',
 '20040816084925.0',
 '990802s2000    mau      b    001 0 eng',
 '(DLC)   99043581',
 '0',
 'vip',
 'orignew',
 '1',
 'ocip',
 '19',
 'y-gencatlg',
 '0',
 'acquire',
 '2 shelf copies',
 'policy default',
 "pc05 to ja00 08-02-99; jf05 to subj. 08/02/99; jf11 to sl 08-03-99; ...",
 'ADDED COPIES: another copy to ASCD ps15 01-12-00',
 '99043581',
 '020161622X',
 'DLC',
 'DLC',
 'DLC',
 'pcc',
 '0',
 'QA76.6',
 '.H857 2000',
 '0',
 '0',
 '005.1',
 '21',
 '0',
 '1',
 'Hunt, Andrew,',
 '1964-',
 '1',
 'The pragmatic programmer :',
 'from journeyman to master /',
 'Andrew Hunt, David Thomas.',
 '4',
 'Reading, Mass :',
 'Addison-Wesley,',
 '2000.',
 'xxiv, 321 p. ;',
 '24 cm.',
 'Includes bibliographical references.',
 'Computer programming.',
 '0',
 '1',
 'Thomas, David,',
 '1956-',
 'GAP']
```

More examples
-------------

Adding a control field (001-009):

```python
>>> import pymarc

>>> # w/ Record
>>> field = pymarc.Field('001', data='12345')
>>> record.add_field(field)

>>> # w/ marcx.Record
>>> record.add('001', data='21345')
```

Adding a non-control field (010-999):

```python
>>> # w/ Record
>>> field = pymarc.Field('852', [' ',' '], subfields = ['a', 'DE-15'])
>>> record.add_field(field)

>>> # w/ Record, [' ',' '] are the default indicators
>>> record.add('852', a='DE-15')
```

Adding multiple subfields to a non-control field at once:

```python
>>> # w/ Record
>>> field = pymarc.Field('980', [' ',' '], subfields=['a', '12376'])
>>> record.add_field(field)
>>> field = pymarc.Field('980', [' ',' '], subfields=['b', '001'])
>>> record.add_field(field)

>>> # w/ marcx.Record
>>> record.add('980', a='12376', b='001')
```

Adding multiple subfields to a non-control field at once with different indicators:

```python
>>> # w/ Record
>>> field = pymarc.Field('041', ['0',' '], subfields=['a', 'ger'])
>>> record.add_field(field)
>>> field = pymarc.Field('041', ['0','7'], subfields=['a', 'dt.'])
>>> record.add_field(field)

>>> # w/ marcx.Record
>>> record.add('041', a='ger', indicators=['0',' '])
>>> record.add('041', a='dt.', indicators=['0','7'])
```

Specify indicators as strings (since an indicator is just a single char):

```python
>>> # w/ marcx.Record
>>> record.add('041', a='ger', indicators='0 ')
>>> record.add('041', a='dt.', indicators='07')
```

Remove a field:

```python
>>> # w/ Record
>>> __001 = record['001']
>>> record.remove_field(__001)

>>> # w/ marcx.Record
>>> record.remove('001') # removes all 001 fields
```

Example from [pymarc.Field](https://github.com/edsu/pymarc/blob/master/pymarc/field.py) source:

```python
>>> # w/ Record
... field = Field(
... tag='245',
... indicators=['0', '1'],
... subfields=[
...     'a', 'The pragmatic programmer : ',
...     'b', 'from journeyman to master /',
...     'c', 'Andrew Hunt, David Thomas.'
... ])
>>> record.add_field(field)

>>> # w/ marcx.Record
>>> record.add('245',
... a='The pragmatic programmer : ',
... b='from journeyman to master /',
... c='Andrew Hunt, David Thomas.',
... indicators='01')
```

Catching basic errors
---------------------

See also: [00X - Control Fields-General Information](http://www.loc.gov/marc/bibliographic/bd00x.html)

```python
>>> obj.add('001', a='Yeah')
...
ValueError: data must not be empty

>>> obj.add('010', data='Yeah')
...
ValueError: non-control fields take no data

>>> obj.add('001', data='...', indicators='00')
...
ValueError: control fields take no indicators
see: http://www.loc.gov/marc/bibliographic/bd00x.html

>>> obj.add('001', data='...', a='X')
...
ValueError: control fields take no subfields
see: http://www.loc.gov/marc/bibliographic/bd00x.html
```

Development
-----------

Easiest way to run the tests is via [nose](https://nose.readthedocs.org/en/latest/):

    $ nosetests
