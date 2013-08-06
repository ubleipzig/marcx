README
======

`marcx.FatRecord` is a small extension to 
[pymarc.Record](https://github.com/edsu/pymarc/blob/056cea129758c20068aec11a4cb148d65987d905/pymarc/record.py#L72), 
that adds a few shortcuts. The gist are the twins 
`add` and `remove`, a (subfield) value generator `itervalues` and a generic `test` function.

[![Build Status](https://travis-ci.org/miku/marcx.png)](https://travis-ci.org/miku/marcx) [![PyPi version](https://pypip.in/v/marcx/badge.png)](https://crate.io/packages/marcx/)

Installation
------------


    $ pip install marcx


Python 2.6 required. If you want to run the tests, too, you'll need 2.7.

Overview
--------

* Create a record:

    ```python
    >>> from marcx import FatRecord
    >>> from marcx import _equals, _startswith, _search, _match, _not
    >>> record = FatRecord()
    ```


**Note** `pymarc.Record` implements subfields via `list`, that means they are
ordered. When using `FatRecord` and `kwargs` to create subfields, you'll
lose order - which in some cases might be of importance. Also multiple subfields
in one field (e.g. multiple places of publication within a single 260 field)
cannot be created with the current `kwargs` mechanism.

* Add and remove fields with one line (control fields get `data`, 
  non-control fields get subfields):

    ```python
    >>> record.add('001', data='12345')
    >>> record.add('020', a='9780201616224')
    >>> record.add('020', a='020161622X')
    >>> record.remove('001')
    ```

* Add repeated subfields:

    ```python
    >>> record.remove('020.a')
    >>> record.add('020', a=('9780201616224', '020161622X'))
    ```

* Add fields with many subfields at once:
    
    ```python
    >>> record.add('990', a='1', b='2', c='3', d='5', e='6')
    ```


* Add numeric subfield with underscores:

    ```python
    >>> record.add('991', _0='Zero', _1='One', _9='Nine')
    ```


* Value iteration via `fieldspec` - a `fieldspec` is just a string, that's
  specifying either a *tag* or a *tag and subfield* combination.

    ```python
    >>> for isbn in record.itervalues('020.a'): print(isbn)
    9780201616224
    020161622X
    ```


* Iterate over multiple fieldspecs at once:

    ```python
    >>> record.add('776', z='0974514055')
    >>> for isbn in record.itervalues('020.a', '776.z'): print(isbn)
    9780201616224
    020161622X
    0974514055
    ```


* Iterate over fields, but instead of just returning the values, return 
  tuples of the form `(fieldobj, value)`:

    ```python
    >>> for fv in record.iterfields('020.a'): print(fv)
    (<pymarc.field.Field object at 0x18e7990>, '9780201616224')
    (<pymarc.field.Field object at 0x18e7990>, '020161622X')
    ```


* Test field and subfield with predicates. Pass any function, that returns
  a boolean value to `test` and it gets evaluated over all values:

    ```python
    >>> if record.test('020', _startswith('978')):
    ...     print('At least one ISBN starts with 978')
    At least one ISBN starts with 978

    >>> record.test('776.z', _startswith('978'))
    False
    ```

* Make sure, all values match the predicate with `all=True`:

    ```python
    >>> if not record.test('020', _startswith('978'), all=True):
    ...     print('Not all ISBNs start with 978')
    Not all ISBNs start with 978
    ```


* One logical operator ships with *marcx*, the unary *not*, so the above could 
  also be written with `_not`, without `_all`:

    ```python
    >>> if record.test('020', _not(_startswith('978'))):
    ...     print('At least one ISBN does not start with 978')
    At least one ISBN does not start with 978
    ```


* Test multiple fieldspecs at once:

    ```python
    >>> record.test('776.z', '020.a', _startswith('978'))
    True
    ```


More examples
-------------

* Adding a control field (001-009):

    ```python
    >>> import pymarc

    >>> # w/ Record
    >>> field = pymarc.Field('001', data='12345')
    >>> record.add_field(field)

    >>> # w/ FatRecord
    >>> record.add('001', data='21345')
    ```

* Adding a non-control field (010-999):

    ```python
    >>> # w/ Record
    >>> field = pymarc.Field('852', [' ',' '], subfields = ['a', 'DE-15'])
    >>> record.add_field(field)

    >>> # w/ FatRecord, [' ',' '] are the default indicators
    >>> record.add('852', a='DE-15')
    ```

* Adding multiple subfields to a non-control field at once:

    ```python
    >>> # w/ Record
    >>> field = pymarc.Field('980', [' ',' '], subfields=['a', '12376'])
    >>> record.add_field(field)
    >>> field = pymarc.Field('980', [' ',' '], subfields=['b', '001'])
    >>> record.add_field(field)
 
    >>> # w/ FatRecord
    >>> record.add('980', a='12376', b='001')
    ```


* Adding multiple subfields to a non-control field at once with different indicators:

    ```python
    >>> # w/ Record
    >>> field = pymarc.Field('041', ['0',' '], subfields=['a', 'ger'])
    >>> record.add_field(field)
    >>> field = pymarc.Field('041', ['0','7'], subfields=['a', 'dt.'])
    >>> record.add_field(field)

    >>> # w/ FatRecord 
    >>> record.add('041', a='ger', indicators=['0',' '])
    >>> record.add('041', a='dt.', indicators=['0','7'])
    ```

* Specify indicators as strings (since an indicator is just a single char):

    ```python
    >>> # w/ FatRecord 
    >>> record.add('041', a='ger', indicators='0 ')
    >>> record.add('041', a='dt.', indicators='07')
    ```

* Removing a field:

    ```python
    >>> # w/ Record
    >>> __001 = record['001']
    >>> record.remove_field(__001)

    >>> # w/ FatRecord
    >>> record.remove('001') # removes all 001 fields
    ```

* Example from [pymarc.Field](https://github.com/edsu/pymarc/blob/master/pymarc/field.py) source:

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

    >>> # w/ FatRecord
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

Higher order functions
----------------------

Functions provided:

    ==                        --> _equals(v)
    re.match()                --> _match(v)
    re.search()               --> _search(v)
    string.startswith(value)  --> _startswith(v)
    string.endswith(value)    --> _endswith(v)

The general structure of these functions is a [closure](http://en.wikipedia.org/wiki/Closure_%28computer_science%29):

```python
def fun(parameter):
    def tester(value):
        # .. whatever's needed
        # return parameter == value
        # return re.match(parameter, value)
        # return value.startswith(parameter)
        return parameter in value:
    return tester
```

It would be great, if we could combine these predicates.
Maybe with some help from [https://github.com/kachayev/fn.py](https://github.com/kachayev/fn.py).


Higher order function in a real world scenario
----------------------------------------------

```python
>>> # ... load data ...
    
>>> __970c = 'OD'

>>> for val in [ v.strip(' []') for v in record.itervalues('250.a') ]:
...     if val in ('Partitur', 'Stimmen', 'Klavierauszug'):
...         __970c = 'DN'
...         break

>>> # examples for various regex patterns
    
>>> centuries = lambda it: _search(r'%s' % '|'.join(it))
>>> if record.test('260.c', centuries( ('15', '16', '17') )):
...     __970c = 'DN'

>>> specified = (
...     'Mus\.pr\.', 
...     'LB Coburg', 
...     'Liturg', 
...     'Hbm/G', 
...     'Hbm/D', 
...     'rar\.', 
...     'St\.th\.', 
...     'Mus\.ms\.', 
...     'Mus\.coll', 
...     'Mus\.N\.'
... )
>>> tester = lambda it: _search(r'%s' % '|'.join(specified))
>>> if record.test('856.3', tester):
...     __970c = 'DN'

>>> specified = (
...     'rar\.',
...     'Mus\.ms\.',
...     'Mus\.N\.'
... )

>>> if record.test('856.3', _search(r'%s' % '|'.join(specified))):
...     record.add('970', d='Quelle')

>>> record.add('970', c=__970c)
```

Development
-----------

Easiest way to run the tests is via [nose](https://nose.readthedocs.org/en/latest/):

    $ nosetests
