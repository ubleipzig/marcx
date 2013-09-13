#!/usr/bin/env python
# coding: utf-8

"""
Few extensions on `pymarc.Record` to make certain checks and manipulations
a bit easier.

Documentation and Examples: https://github.com/miku/marcx
"""

from pymarc.exceptions import FieldNotFound
from pymarc.record import Record, Field
import collections
import itertools
import pyisbn
import re

__version__ = '0.1.9'

__all__ = [
    'FatRecord',
    '_equals',
    '_not',
    '_match',
    '_search',
    '_startswith',
    '_endswith',
    'valuegetter',
    'fieldgetter',
    'FincMarc',
]


def pairwise(iterable):
    """
    s -> (s0, s1), (s2, s3), (s4, s5), ...
    """
    it = iter(iterable)
    return itertools.izip(it, it)


def _equals(value):
    """
    Equality test.
    """
    return lambda v: value == v


def _not(value):
    """
    Usage example: `_not(_equal(...))`.
    """
    if hasattr(value, '__call__'):
        return lambda v: not value(v)
    else:
        return lambda v: not v


def _match(value):
    """
    Maps to `re.match` (match at the beginning of `v`).
    """
    return lambda v: re.match(value, v)


def _search(value):
    """
    Maps to `re.search` (match anywhere in `v`).
    """
    return lambda v: re.search(value, v)


def _startswith(value):
    """
    Maps to `string.startswith`.
    """
    return lambda v: v.startswith(value)


def _endswith(value):
    """
    Maps to `string.endswith`.
    """
    return lambda v: v.endswith(value)


def valuegetter(*fieldspecs, **kwargs):
    """
    Modelled after `operator.itemgetter`. Takes a variable
    number of specs and returns a function, which applied to
    any `pymarc.Record` returns the matching values.

    Specs are in the form `field` or `field.subfield`, e.g.
    `020` or `020.9`.

    Example:

    >>> from marcx import FatRecord, valuegetter
    >>> from urllib import urlopen
    >>> record = FatRecord(data=urlopen("http://goo.gl/lfJnw9").read())

    In two steps:

    >>> getter = valuegetter('020.a')
    >>> getter(record)
    <generator object values at 0x2d97690>

    >>> set(getter(record))
    set(['020161622X'])

    Or in one step:

    >>> set(valuegetter('020.a')(record))
    set(['020161622X'])

    A variable number of specs can be passed:

    >>> set(valuegetter('001', '005', '700.a')(record))
    set(['20040816084925.0', 'Thomas, David,', '11778504'])

    Non-existent field tags can be passed - they are ignored:
    >>> set(valuegetter('002')(record))
    set([])

    @see also: `FatRecord.itervalues`
    """
    combine_subfields = kwargs.get('combine_subfields', False)
    pattern = r'(?P<field>[^.]+)(.(?P<subfield>[^.]+))?'

    def values(record):
        for s in fieldspecs:
            match = re.match(pattern, s)
            if not match:
                continue
            gd = match.groupdict()
            for field in record.get_fields(gd['field']):
                if gd['subfield']:
                    for value in field.get_subfields(gd['subfield']):
                        yield value
                else:
                    if combine_subfields:
                        yield field.value()
                    else:
                        if int(gd['field']) < 10:
                            yield field.value()
                        else:
                            for value in field.subfields[1::2]:
                                yield value
    values.__doc__ = 'returns a value generator over %s' % (
        ', '.join(fieldspecs))
    return values


def fieldgetter(*fieldspecs):
    """
    Similar to `valuegetter`, except this returns (`pymarc.Field`, value)
    tuples. Takes any number of fieldspecs.
    """
    pattern = r'(?P<field>[^.]+)(.(?P<subfield>[^.]+))?'

    def fields(record):
        for s in fieldspecs:
            match = re.match(pattern, s)
            if not match:
                continue
            grp = match.groupdict()
            for field in record.get_fields(grp['field']):
                if grp['subfield']:
                    for value in field.get_subfields(grp['subfield']):
                        yield field, value
                else:
                    if int(grp['field']) < 10:
                        yield field, field.value()
                    else:
                        for value in field.subfields[1::2]:
                            yield field, value
    fields.__doc__ = 'returns a field generator over %s' % (
        ', '.join(fieldspecs))
    return fields


class FatRecord(Record):
    """
    A record with some extras.
    """
    CONTROL_FIELDS = set(
        ('001', '002', '003', '004', '005', '006', '007', '008', '009'))

    E_NO_INDICATORS = """control fields take no indicators
    see: http://www.loc.gov/marc/bibliographic/bd00x.html"""
    E_NO_SUBFIELDS = """control fields take no subfields
    see: http://www.loc.gov/marc/bibliographic/bd00x.html"""
    E_NO_DATA = "non-control fields take no data"
    E_EMPTY = "data must not be empty"
    E_INVALID_INDICATOR = "invalid indicator"

    def __init__(self, *args, **kwargs):
        super(FatRecord, self).__init__(*args, **kwargs)

    @classmethod
    def from_record(cls, record):
        """
        Factory methods to create FatRecord from pymarc.Record object.
        """
        if not isinstance(record, Record):
            raise TypeError('record must be of type pymarc.Record')
        record.__class__ = FatRecord
        return record

    def to_record(self):
        """
        Convert FatRecord to a pymarc.Record class. This is partially
        addressed in https://github.com/edsu/pymarc/pull/36.
        """
        self.__class__ = Record
        return self

    def add(self, tag, data=None, indicators=None, **kwargs):
        """
        Add a field to a record. Example:

        marc.add('020', a='0201657880', z='0201802398')
        """
        if data:
            if indicators:
                raise ValueError(FatRecord.E_NO_INDICATORS)
            if not tag in FatRecord.CONTROL_FIELDS:
                raise ValueError(FatRecord.E_NO_DATA)
        else:
            if tag in FatRecord.CONTROL_FIELDS:
                raise ValueError(FatRecord.E_EMPTY)

        if tag in FatRecord.CONTROL_FIELDS and kwargs:
            raise ValueError(FatRecord.E_NO_SUBFIELDS)

        if indicators is None:
            indicators = [' ', ' ']
        if isinstance(indicators, basestring):
            if len(indicators) == 2:
                indicators = [indicators[0], indicators[1]]
            else:
                raise ValueError(FatRecord.E_INVALID_INDICATOR)

        if data:  # == control field (001 -- 009)
            field = Field(tag, data=data)
        else:     # == non-control field (010 -- 999)
            subfields = []
            for key, value in kwargs.iteritems():
                key = key.replace('_', '')
                if isinstance(value, basestring):
                    subfields += [key, value]
                elif isinstance(value, collections.Iterable):
                    for val in value:
                        if not isinstance(val, basestring):
                            raise ValueError('subfield values must be strings')
                        subfields += [key, val]
                else:
                    raise ValueError('subfield values must be strings')
            field = Field(tag, indicators, subfields=subfields)
        self.add_field(field)

    def remove(self, fieldspec):
        """
        Removes fields or subfields according to `fieldspec`.

        If a non-control field subfield removal leaves no other subfields,
        delete the field entirely.
        """

        pattern = r'(?P<field>[^.]+)(.(?P<subfield>[^.]+))?'
        match = re.match(pattern, fieldspec)
        if not match:
            return None

        grp = match.groupdict()
        for field in self.get_fields(grp['field']):
            if grp['subfield']:
                updated = []
                for code, value in pairwise(field.subfields):
                    if not code == grp['subfield']:
                        updated += [code, value]
                # if we removed the last subfield entry,
                # remove the whole field, too
                if not updated:
                    self.remove_field(field)
                else:
                    field.subfields = updated
            else:
                # it is a control field
                self.remove_field(field)

    def firstvalue(self, *fieldspecs, **kwargs):
        """
        Return the [first] [v]alue or the value given by the keyword
        argument `default` if not value exists. `default` defaults to `None`.
        """
        default = kwargs.get('default', None)
        values = [val for val in self.itervalues(*fieldspecs, **kwargs)]
        if values:
            return values[0]
        else:
            return default

    def itervalues(self, *fieldspecs, **kwargs):
        """
        Apply valuegetter on self.
        Shortcut for `valuegetter(*fieldspecs)(self)`
        """
        return valuegetter(*fieldspecs, **kwargs)(self)

    def iterfields(self, *fieldspecs):
        """
        Shortcut for `fieldgetter(*fieldspecs)(self)`
        """
        return fieldgetter(*fieldspecs)(self)

    def remove_field_if(self, *args):
        """
        Remove a field from this record, if
        `fun(value)` evaluates to `True`.

        The real signature is like:

            remove_field_if(self, fieldspec, fun):

        but a variable number of fieldspecs can be added,
        so we have to resort to `*args` and figure out, which one is
        a function, by asking if the argument is `callable`.

        Example:

        Iterate over all 710.a fields and remove the
        field, if any subfield value startswith
        'Naxos Digital Services.'

        Returns a list of removed fields (or an empty list).

        >>> _ = record.remove_field_if('710.a',
            _startswith('Naxos Digital Services.'))

        If there are multiple fields with the same tag,
        only the fields that match are removed, e.g.:

        >>> record = FatRecord()
        >>> record.add('020', a='97811111111')
        >>> record.add('020', a='11111111')
        >>> rmvd = record.remove_field_if('020.a', _startswith('978'))
        >>> print(rmvd)
        [<pymarc.field.Field object at 0x1e53910>]

        >>> print(record)
        =LDR            22        4500
        =020  \\$a11111111

        """
        fieldspecs = set()
        function = lambda val: False
        for arg in args:
            if callable(arg):
                function = arg
            elif isinstance(arg, basestring):
                fieldspecs.add(arg)
            else:
                raise ValueError('argument must be callable (test function) '
                                 'or basestring (fieldspec, like 020 '
                                 'or 856.u, etc.)')
        removed = []
        for field, value in fieldgetter(*fieldspecs)(self):
            if function(value):
                removed.append(field)
                self.remove_field(field)
        return removed

    def test(self, *args, **kwargs):
        """
        Test whether the function evaluated on the fields given in `args`
        returns `True`.

        >>> record.add('020.a', a='0387310738', z='1234')
        >>> def _is_valid_isbn(value):
        ...     ''' poor man's isbn validator '''
        ...     return len(value) in (10, 13)
        >>> record.test('020.a', '020.z', _is_valid_isbn)
        True

        If `all` is set to `True`, the test only
        returns `True`, if all values pass the given check, e.g.:

        >>> record.test('020.a', '020.z', _is_valid_isbn, all=True)
        False

        means that for each field and every value the ISBN check
        is performed. Defaults to `False`.

        """
        fieldspecs = set()
        function = lambda val: True
        for arg in args:
            if callable(arg):
                function = arg
            elif isinstance(arg, basestring):
                fieldspecs.add(arg)
            else:
                raise ValueError('argument must be callable (test function) '
                                 'or basestring (fieldspec, like 020.a '
                                 'or 856.u, etc.)')
        if kwargs.get('all', False):
            return min(
                [function(value) for value in valuegetter(*fieldspecs)(self)])
        else:
            for value in valuegetter(*fieldspecs)(self):
                if function(value):
                    return True
        # all is False and none of the values passed the test
        return False

    def has(self, fieldspec):
        """
        Return `True` is the record has any value in the specified fieldspec.
        """
        return bool(len(set(self.itervalues(fieldspec))) > 0)

    def flatten(self):
        """
        Flatten this record to a simple list of values
        (from all fields, except the leader).
        """
        d = self.as_dict()
        del d['leader']
        return [s for s in [v.strip() for v in flatten(d)] if s]


def flatten(struct):
    """Cleates a flat list of all items in structured output (dicts, lists, items)
    Examples:
    > _flatten({'a': foo, b: bar})
    [foo, bar]
    > _flatten([foo, [bar, troll]])
    [foo, bar, troll]
    > _flatten(foo)
    [foo]
    """
    if struct is None:
        return []
    flat = []
    if isinstance(struct, dict):
        for key, result in struct.iteritems():
            flat += flatten(result)
        return flat

    if isinstance(struct, basestring):
        return [struct]

    try:
        # if iterable
        for result in struct:
            flat += flatten(result)
        return flat
    except TypeError:
        pass

    return [struct]


def isbn_convert(isbn_10_or_13):
    """
    Return the *other* ISBN representation. Returns `None`
    if conversion fails.
    """
    try:
        return pyisbn.convert(isbn_10_or_13)
    except pyisbn.IsbnError as _:
        pass


class FincMarc(FatRecord):
    """
    Add a few FINC project specific details to `FatRecord`.
    """
    def __init__(self, *args, **kwargs):
        super(FincMarc, self).__init__(*args, **kwargs)
        self.sigels = set()
        self.source_id = None
        self.record_id = None

    @classmethod
    def from_doc(cls, doc, **kwargs):
        """
        Create a FatRecord from a dictionary as it is
        stored in Elasticsearch.

        Elasticsearch JSON > dict > FatRecord

        Keyword arguments used:

        * encoding      [utf-8]
        * to_unicode    [True]
        * force_utf8    [True]

        Example doc:

        {
            "content": {
                "830":[
                    {
                        "w":"(DE-576)027236307",
                        "g":"15",
                        "v":"15",
                        "a":"Hauterive-Champréveyres",
                        "ind2":"0",
                        "ind1":" "
                    },
                    {
                        "w":"(DE-576)017312833",
                        "v":"40",
                        "a":"Archéologie neuchâteloise",
                        "ind2":"0",
                        "ind1":" "
                    }
                ],
                "300":[
                    {
                        "b":"Ill., graph. Darst., Kt.",
                        "a":"163, 39 S. :",
                        "ind2":" ",
                        "ind1":" "
                    }
                ],
                "260": ...
            ...
            "original":"00919cam a2200253  b4500001001000..."
            "sha1":"bd8d3f250d2c8cb210dbb6323240b897f48ddcac",
            "content_type":"application/marc",
            "meta": {
                "tags":[
                    "da88ecbc0c348fc1f232a41d435c04bd974f390b"
                ],
                "timestamp":"201302071200",
                ...
            }
        }
        """
        assert(isinstance(doc, dict))
        encoding = kwargs.get('encoding', 'utf-8')
        to_unicode = kwargs.get('to_unicode', True)
        force_utf8 = kwargs.get('force_utf8', True)
        if not 'original' in doc:
            raise ValueError('document without `original` key')
        original = doc.get('original', '').encode(encoding)
        return FatRecord(data=original, to_unicode=to_unicode,
                         force_utf8=force_utf8)

    def get_control_number(self):
        """
        Return the control number value.
        Raises `AttributeError` on missing value.
        """
        return self['001'].value()

    def set_control_number(self, value):
        """
        Set the control number.
        """
        current = self['001']
        try:
            self.remove_field(current)
        except FieldNotFound as fnf:
            pass
        self.add('001', data=value)

    # alias control_number to finc_id
    control_number = property(get_control_number, set_control_number)
    finc_id = control_number

    def isbn_candidates(self, *fieldspecs):
        """
        Class `pymarc.Record` only has an `isbn` attribute
        (returns the first 020.a value). The fat record can take
        a fieldspec. If no fieldspec is given, use `020.a`.

        Returns a `set` of candidates.
        """
        if not fieldspecs:
            fieldspecs = ('020.a',)
        return set(valuegetter(*fieldspecs)(self))

    def isbns(self, *fieldspecs):
        """
        Return checked ISBN candidates as `set`.
        """
        result = set()
        for candidate in self.isbn_candidates(*fieldspecs):
            candidate = (candidate.split() or [""])[0]
            candidate = candidate.replace('-', '')
            if len(candidate) in (10, 13):
                if pyisbn.validate(candidate):
                    result.add(candidate)
        return result

    def grow_isbns(self):
        """
        Special routine to grow ISBN from various fields and to complement
        all 10-char versions with their 13-char versions and vice versa.

        An ISBN can be found in:

            020.a   International Standard Book Number (R)
                    http://www.loc.gov/marc/bibliographic/bd020.html

            020.z   $z - Canceled/invalid ISBN (R)

            020.9   unspecified

            776.z   776 - Additional Physical Form Entry (R)
                    $z - International Standard Book Number (R)
        """
        isbns = self.isbns('020.a')

        for isbn in isbns.copy():
            alt = isbn_convert(isbn)
            if alt and alt not in isbns:
                self.add('020', a=alt)
                isbns.add(alt)

        # stash cancelled isbns add additional entries into 020.z
        cancelled = self.isbns('020.z', '020.9')
        additional = self.isbns('776.z')
        isbns.update(cancelled | additional)

        for isbn in cancelled | additional:
            alt = isbn_convert(isbn)
            if alt and alt not in isbns:
                self.add('020', z=alt)
                isbns.add(alt)

        return isbns
