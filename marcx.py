#!/usr/bin/env python
# coding: utf-8

"""
Few extensions on `pymarc.Record` to make certain checks
and manipulations a bit easier.
"""

import collections
import itertools
import re
import warnings
from builtins import zip

import jsonpath_rw as jpath
import pymarc
from past.builtins import basestring

__version__ = '0.2.2'

__all__ = [
    'Record',
    'FatRecord',  # Deprecated, use Record instead.
    'marcdoc',
    'valuegetter',
    'fieldgetter',
]


class DotDict(dict):
    """ Dot access for dictionaries. """

    def __init__(self, d=None, **kwargs):
        if d is None:
            d = {}
        if kwargs:
            d.update(**kwargs)
        for k, v in list(d.items()):
            setattr(self, k, v)
        for k in list(self.__class__.__dict__.keys()):
            if not (k.startswith('__') and k.endswith('__')):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if isinstance(value, (list, tuple)):
            value = [self.__class__(x) if isinstance(x, dict) else x for x in value]
        else:
            value = self.__class__(value) if isinstance(value, dict) else value
        super(DotDict, self).__setattr__(name, value)
        self[name] = value


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


def pairwise(iterable):
    """
    s -> (s0, s1), (s2, s3), (s4, s5), ...
    """
    it = iter(iterable)
    return zip(it, it)


def valuegetter(*fieldspecs, **kwargs):
    """
    Modelled after `operator.itemgetter`. Takes a variable
    number of specs and returns a function, which applied to
    any `pymarc.Record` returns the matching values.

    Specs are in the form `field` or `field.subfield`, e.g.
    `020` or `020.9`.

    Example:

    >>> from marcx import Record, valuegetter
    >>> from urllib import urlopen
    >>> record = Record(data=urlopen("http://goo.gl/lfJnw9").read())

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

    @see also: `Record.itervalues`
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


class Record(pymarc.Record):
    """
    A record with some extras.
    """
    E_NO_INDICATORS = """control fields take no indicators
    see: http://www.loc.gov/marc/bibliographic/bd00x.html"""
    E_NO_SUBFIELDS = """control fields take no subfields
    see: http://www.loc.gov/marc/bibliographic/bd00x.html"""
    E_NO_DATA = "non-control fields take no data"
    E_EMPTY = "data must not be empty"
    E_INVALID_INDICATOR = "invalid indicator"

    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args, **kwargs)

    @classmethod
    def from_record(cls, record):
        """
        Factory methods to create Record from pymarc.Record object.
        """
        if not isinstance(record, pymarc.Record):
            raise TypeError('record must be of type pymarc.Record')
        record.__class__ = Record
        return record

    def to_record(self):
        """
        Convert Record to a pymarc.Record class. This is partially
        addressed in https://github.com/edsu/pymarc/pull/36.
        """
        self.__class__ = pymarc.Record
        return self

    def add(self, tag, data=None, indicators=None, **kwargs):
        """
        Add a field to a record. Example:

        marc.add('020', a='0201657880', z='0201802398')
        """
        if data:
            if indicators:
                raise ValueError(Record.E_NO_INDICATORS)
            if not tag.startswith('00'):
                raise ValueError(Record.E_NO_DATA)
        else:
            if tag.startswith('00'):
                raise ValueError(Record.E_EMPTY)

        if tag.startswith('00') and kwargs:
            raise ValueError(Record.E_NO_SUBFIELDS)

        if indicators is None:
            indicators = [' ', ' ']
        if isinstance(indicators, basestring):
            if len(indicators) == 2:
                indicators = [indicators[0], indicators[1]]
            else:
                raise ValueError(Record.E_INVALID_INDICATOR)

        if data:  # == control field (001 -- 009)
            field = pymarc.Field(tag, data=data)
        else:     # == non-control field (010 -- 999)
            subfields = []
            for key, value in kwargs.items():
                if value is None:
                    continue
                key = key.replace('_', '')
                if isinstance(value, basestring):
                    if value == "":
                        continue
                    subfields += [key, value]
                elif isinstance(value, collections.Iterable):
                    for val in value:
                        if not isinstance(val, basestring):
                            raise ValueError('subfield values must be strings')
                        subfields += [key, val]
                else:
                    raise ValueError('subfield values must be strings')
            field = pymarc.Field(tag, indicators, subfields=subfields)
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

        >>> record = Record()
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

FatRecord = Record


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
        for key, result in struct.items():
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


class marcdoc(dict):
    """ A wrapper around an dictionary that represents a MARC record.

    Example document:

        doc = {
            "_index" : "bsz",
            "_type" : "title",
            "_id" : "036937401",
            "_score" : 1.0,

            "_source" : {
                "content": {
                    "245": [{"a": "De induratione hepatis /", ... } ],
                    ...
                },
                "meta": {"date": "2014-03-04"}
            }
        }

    Usage:

        md = marcx.marcdoc(doc)
        isbns = ', '.join(itertools.chain(md.x020a, md.x020z, md.x0209,
                                          md.x776z))
    """

    def __init__(self, document, default_prefix='_source', default_index='*'):
        warnings.warn("deprecated", DeprecationWarning)
        dict.__init__(self, document)
        self.document = document
        self.expression_cache = {}
        self.default_prefix = default_prefix
        self.default_index = default_index

    def tag_to_expression(self, tag, prefix=None, index=None):
        """ Return a multivalued parser for the given tag (e.g. 020 or 700.a).
        """
        if prefix is None:
            prefix = self.default_prefix
        if index is None:
            index = self.default_index
        tag = tag.replace('.', '').strip()
        if 3 > len(tag) > 4:
            raise ValueError('tag must be of the form 008, 020a or 020.a')
        if len(tag) == 4:
            tag, code = tag[:3], tag[3:]
            return jpath.parse('{prefix}.content["{tag}"]'
                               '[{index}].["{code}"]'.format(prefix=prefix,
                                                             tag=tag, index=index, code=code))
        else:
            return jpath.parse('{prefix}.content["{tag}"]'.format(prefix=prefix,
                                                                  tag=tag))

    def isbns(self):
        return itertools.chain(self.x020a, self.x020z, self.x0209, self.x776z)

    def values(self, *args):
        result = []
        for arg in args:
            if arg not in self.expression_cache:
                self.expression_cache[arg] = self.tag_to_expression(arg)
            expression = self.expression_cache[arg]
            if len(arg) > 3:
                result += flatten([m.value for m in expression.find(self.document)])
            else:
                result += [m.value for m in expression.find(self.document)]
        return result

    def __getattr__(self, name):
        """ Dynamic attribute lookup. Converts `obj.x020a` attribute
        into a jsonpath expression, evaluates it the document and
        returns a *list* of values. Expressions are lazily evaluated.

        Cannot start an attribute with a digit, so the first character
        needs to be some letter.
        """
        try:
            tag = name[1:]
            if tag not in self.expression_cache:
                self.expression_cache[tag] = self.tag_to_expression(tag)
            expression = self.expression_cache[tag]
            if len(tag) > 3:
                return flatten([m.value for m in expression.find(self.document)])
            else:
                return [m.value for m in expression.find(self.document)]
        except Exception as exc:
            raise AttributeError(exc)
