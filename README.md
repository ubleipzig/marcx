README
======

*marcx* is a small extension to [pymarc.Record](https://github.com/edsu/pymarc/blob/master/pymarc/record.py#L72), that adds
a few shortcuts. The gist are the twins `add` and `remove` and generic `test`
function.

Examples
--------

    from marcx import FatRecord, _startswith
    record = FatRecord(data=...)

* Add and remove fields with one line

        record.remove('001')
        record.add('001', data='12345')
        record.add('020', a='020161622X')

* Value iteration via `fieldspec` - a `fieldspec` is just a string, that's
  specifying either a tag or a tag and subfield combination.

        for isbn in record.vg('020.a'):
            # do something

        for vals in record.vg('020', 700.a', '856.x'):
            # do something

* Tests

        if record.test('020', _startswith('02016')):
            # do something


More examples
-------------

* Adding a control field (001-009):

        # w/ Record
        field = pymarc.Field('001', data='12345')
        record.add_field(field)

        # w/ FatRecord
        record.add('001', data='21345')

* Adding a non-control field (010-999):

        # w/ Record
        field = pymarc.Field('852', [' ',' '], subfields = ['a', 'DE-15'])
        record.add_field(field)

        # w/ FatRecord, [' ',' '] are the default indicators
        record.add('852', a='DE-15')

* Adding multiple subfields to a non-control field at once:

        # w/ Record
        field = pymarc.Field('980', [' ',' '], subfields=['a', '12376'])
        record.add_field(field)
        field = pymarc.Field('980', [' ',' '], subfields=['b', '001'])
        record.add_field(field)

        # w/ FatRecord
        record.add('980', a='12376', b='001')


* Adding multiple subfields to a non-control field at once with different indicators:

        # w/ Record
        field = pymarc.Field('041', ['0',' '], subfields=['a', 'ger'])
        record.add_field(field)
        field = pymarc.Field('041', ['0','7'], subfields=['a', 'dt.'])
        record.add_field(field)

        # w/ FatRecord 
        record.add('041', a='ger', indicators=['0',' '])
        record.add('041', a='dt.', indicators=['0','7'])

* Specify indicators as strings (since an indicator is just a single char):

        # w/ FatRecord 
        record.add('041', a='ger', indicators='0 ')
        record.add('041', a='dt.', indicators='07')

* Removing a field:

        # w/ Record
        __001 = record['001']
        record.remove_field(__001)

        # w/ FatRecord
        record.remove('001') # removes all 001 fields

* Example from [pymarc.Field](https://github.com/edsu/pymarc/blob/master/pymarc/field.py) source:

        # w/ Record
        field = Field(
            tag='245', 
            indicators=['0', '1'], 
            subfields=[
                'a', 'The pragmatic programmer : ', 
                'b', 'from journeyman to master /', 
                'c', 'Andrew Hunt, David Thomas.' 
            ])
        record.add_field(field)

        # w/ FatRecord
        record.add('245', 
            a='The pragmatic programmer : ', 
            b='from journeyman to master /', 
            c='Andrew Hunt, David Thomas.', 
            indicators='01')

Catching basic errors
---------------------

See also: [00X - Control Fields-General Information](http://www.loc.gov/marc/bibliographic/bd00x.html)

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


Higher order functions
----------------------

Functions provided:

    ==                        --> _equals(v)
    re.match()                --> _match(v)
    re.search()               --> _search(v)
    string.startswith(value)  --> _startswith(v)
    string.endswith(value)    --> _endswith(v)

The general structure of these functions is a [closure](http://en.wikipedia.org/wiki/Closure_%28computer_science%29):

    def fun(parameter):
        def tester(value):
            # .. whatever's needed
            # return parameter == value
            # return re.match(parameter, value)
            # return value.startswith(parameter)
            return parameter in value:
        return tester

It would be great, if we could combine these predicates.
Maybe with some help from [https://github.com/kachayev/fn.py](https://github.com/kachayev/fn.py).


HOF in real
-----------

    __970c = 'OD'

    for val in record.vg('250.a'):
        if val.strip(' []') in ['Partitur', 'Stimmen', 'Klavierauszug']:
            __970c = 'DN'
            break

    if record.test('260.c', _search(r'15|16|17')):
        __970c = 'DN'

    if record.test('856.3', _search(
        r'Mus\.pr\.|LB Coburg|Liturg|Hbm/G|Hbm/D|rar\.|St\.th\.|Mus\.ms\.|Mus\.coll|Mus\.N\.')):
            __970c = 'DN'

    if record.test('856.3', _search(r'rar\.|Mus\.ms\.|Mus\.N\.')):
        record.add('970', d='Quelle')

    record.add('970', c=__970c)
