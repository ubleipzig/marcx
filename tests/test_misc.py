#!/usr/bin/env python
# coding: utf-8
# pylint: disable=C0111

import base64
import unittest
from builtins import range

import pymarc
from pymarc import Field, Subfield

import marcx

# helper, shortcut
L = pymarc.field.Field.convert_legacy_subfields

# 00909cas a2200265   4500
# 001 000119652
# 003 DE-576
# 005 20120615084520.0
# 007 tu
# 008 850101c19uuuuuuxx    m            0ger c
# 016    $a (OCoLC)309922781
# 035    $a (DE-599)BSZ000119652
# 040    $a DE-576 $b ger $c DE-576 $e rakwb
# 041 0  $a ger
# 041 07 $a dt.
# 084    $a GL 9346 $2 rvk
# 110 2  $a Adalbert-Stifter-Institut des Landes Oberösterreich $9 g:Linz
#        $0 (DE-588)2003604-8 $0 (DE-576)19159427X
# 245 10 $a Schriftenreihe des Adalbert-Stifter-Institutes
#           des Landes Oberösterreich
# 260    $a Linz : $b Oberoesterr. Landesverl.
# 591    $a 5090, 5550: FRUB11/Sred
# 689 00 $D p $0 (DE-588)118618156 $0 (DE-576)163200580 $2 gnd
#        $a Stifter, Adalbert
# 689 0  $5 DE-576
# 785 00 $i Ab Bd. 42 u.d.T. $t Beiträge zur Stifterforschung
#        $w (DE-576)262359677
# 935    $b druck
# 936 rv $a GL 9346 $b Sekundärliteratur. $0 201559404
MARCREC = base64.b64decode("""
                           MDA5MDljYXMgYTIyMDAyNjUgICA0NTAwMDAxMDAxMDAwMDAwMDAzMDAwNzAwMDEwMDA1MDAxNzAwMDE3
                           MDA3MDAwMzAwMDM0MDA4MDA0MTAwMDM3MDE2MDAyMTAwMDc4MDM1MDAyNTAwMDk5MDQwMDAzMTAwMTI0
                           MDQxMDAwODAwMTU1MDQxMDAwODAwMTYzMDg0MDAxNzAwMTcxMTEwMDEwNDAwMTg4MjQ1MDA3OTAwMjky
                           MjYwMDAzNzAwMzcxNTkxMDAyODAwNDA4Njg5MDA2ODAwNDM2Njg5MDAxMTAwNTA0Nzg1MDA3MzAwNTE1
                           OTM1MDAxMDAwNTg4OTM2MDA0NTAwNTk4HjAwMDExOTY1Mh5ERS01NzYeMjAxMjA2MTUwODQ1MjAuMB50
                           dR44NTAxMDFjMTl1dXV1dXV4eCAgICBtICAgICAgICAgICAgMGdlciBjHiAgH2EoT0NvTEMpMzA5OTIy
                           NzgxHiAgH2EoREUtNTk5KUJTWjAwMDExOTY1Mh4gIB9hREUtNTc2H2JnZXIfY0RFLTU3Nh9lcmFrd2Ie
                           MCAfYWdlch4wNx9hZHQuHiAgH2FHTCA5MzQ2HzJydmseMiAfYUFkYWxiZXJ0LVN0aWZ0ZXItSW5zdGl0
                           dXQgZGVzIExhbmRlcyBPYmVyb8yIc3RlcnJlaWNoHzlnOkxpbnofMChERS01ODgpMjAwMzYwNC04HzAo
                           REUtNTc2KTE5MTU5NDI3WB4xMB9hU2NocmlmdGVucmVpaGUgZGVzIEFkYWxiZXJ0LVN0aWZ0ZXItSW5z
                           dGl0dXRlcyBkZXMgTGFuZGVzIE9iZXJvzIhzdGVycmVpY2geICAfYUxpbnogOh9iT2Jlcm9lc3RlcnIu
                           IExhbmRlc3ZlcmwuHiAgH2E1MDkwLCA1NTUwOiBGUlVCMTEvU3JlZB4wMB9EcB8wKERFLTU4OCkxMTg2
                           MTgxNTYfMChERS01NzYpMTYzMjAwNTgwHzJnbmQfYVN0aWZ0ZXIsIEFkYWxiZXJ0HjAgHzVERS01NzYe
                           MDAfaUFiIEJkLiA0MiB1LmQuVC4fdEJlaXRyYcyIZ2UgenVyIFN0aWZ0ZXJmb3JzY2h1bmcfdyhERS01
                           NzYpMjYyMzU5Njc3HiAgH2JkcnVjax5ydh9hR0wgOTM0Nh9iU2VrdW5kYcyIcmxpdGVyYXR1ci4fMDIw
                           MTU1OTQwNB4d""".replace("\n", ""))


class RecordTests(unittest.TestCase):

    def test_init(self):
        r = marcx.Record()
        self.assertIsNotNone(r)

    def test_constructor(self):
        obj = marcx.Record()
        self.assertIsNotNone(obj)

    def test_superclass(self):
        obj = marcx.Record()
        self.assertTrue(isinstance(obj, pymarc.Record))

    def test_constructor_passes_data(self):
        # data='', to_unicode=False, force_utf8=False,
        # hide_utf8_warnings=False, utf8_handling='strict'
        obj = marcx.Record(data=MARCREC, to_unicode=True, force_utf8=True)
        self.assertEqual(obj.as_marc(), MARCREC)

    def test_add_field_fast(self):
        obj = marcx.Record()
        obj.add('980', a='81723')
        self.assertEqual(['81723'], obj['980'].get_subfields('a'))

        obj.add('981', a='A', b='B', c='C')
        self.assertEqual(['A'], obj['981'].get_subfields('a'))
        self.assertEqual(['B'], obj['981'].get_subfields('b'))
        self.assertEqual(['C'], obj['981'].get_subfields('c'))

    def test_add_indicator(self):
        obj = marcx.Record()
        obj.add('980', a='81723', indicators=['0', ' '])
        self.assertEqual(['0', ' '], obj['980'].indicators)
        self.assertEqual('0', obj['980'].indicator1)
        self.assertEqual(' ', obj['980'].indicator2)

    def test_add_two_fields(self):
        obj = marcx.Record()
        obj.add('041', a='ger', indicators=['0', ' '])
        obj.add('041', a='dt.', indicators=['0', '7'])

        self.assertEqual(2, len(obj.get_fields('041')))
        self.assertEqual(['ger'], obj['041'].get_subfields('a'))
        self.assertEqual(['ger', 'dt.'],
                         [f['a'] for f in obj.get_fields('041')])

        self.assertEqual([['0', ' '], ['0', '7']],
                         [f.indicators for f in obj.get_fields('041')])

    def test_add_control_field(self):
        obj = marcx.Record()
        obj.add('001', data='129')
        self.assertEqual('129', obj['001'].value())

        with self.assertRaises(ValueError):
            obj.add('010', data='129')

        with self.assertRaises(ValueError):
            obj.add('001', data='helo', c='hello')

    def test_accepts_strings_as_indicators(self):
        obj = marcx.Record()
        obj.add('980', a='81723', indicators='0 ')
        self.assertEqual(['0', ' '], obj['980'].indicators)
        self.assertEqual('0', obj['980'].indicator1)
        self.assertEqual(' ', obj['980'].indicator2)

        obj.add('981', a='81723', indicators='07')
        self.assertEqual(['0', '7'], obj['981'].indicators)
        self.assertEqual('0', obj['981'].indicator1)
        self.assertEqual('7', obj['981'].indicator2)

    def test_does_not_ignore_invalid_indicator_strings(self):
        obj = marcx.Record()
        with self.assertRaises(ValueError):
            obj.add('980', a='81723', indicators='Welcome')

    def test_remove_single(self):
        obj = marcx.Record()
        obj.add('001', data='123')
        self.assertEqual(1, len(obj.get_fields('001')))
        obj.remove('001')
        self.assertEqual(0, len(obj.get_fields('001')))

    def test_remove_all(self):
        obj = marcx.Record()
        obj.add('001', data='123')
        obj.add('001', data='456')
        self.assertEqual(2, len(obj.get_fields('001')))
        obj.remove('001')
        self.assertEqual(0, len(obj.get_fields('001')))

    def test_vs_slim_vs_record(self):
        # w/ Record
        record = pymarc.Record()
        field = pymarc.field.Field(
            tag='245',
            indicators=['0', '1'],
            subfields=L([
                'a', 'The pragmatic programmer : ',
                'b', 'from journeyman to master /',
                'c', 'Andrew Hunt, David Thomas.'
            ]))
        record.add_field(field)

        # w/ SlimRecord
        obj = marcx.Record()
        obj.add('245',
                a='The pragmatic programmer : ',
                b='from journeyman to master /',
                c='Andrew Hunt, David Thomas.',
                indicators='01')

        self.assertEqual(len(obj.get_fields('245')),
                          len(record.get_fields('245')))

        self.assertEqual(
            obj.get_fields('245')[0].get_subfields('a'),
            record.get_fields('245')[0].get_subfields('a')
        )

        self.assertEqual(
            obj.get_fields('245')[0].get_subfields('b'),
            record.get_fields('245')[0].get_subfields('b')
        )

        self.assertEqual(
            obj.get_fields('245')[0].get_subfields('c'),
            record.get_fields('245')[0].get_subfields('c')
        )

        # NOTE: this might fail, although the only difference
        # is in the subfield ordering (hashing effect)
        # self.assertEqual(
        #     obj.get_fields('245')[0].__str__(),
        #     record.get_fields('245')[0].__str__()
        # )

    def test_get_first_value(self):
        obj = marcx.Record(data=MARCREC, to_unicode=True, force_utf8=True)
        self.assertEqual(obj.firstvalue('041.a'), 'ger')
        self.assertEqual(obj.firstvalue('260.a'), 'Linz :')
        self.assertEqual(obj.firstvalue('999.9'), None)
        self.assertEqual(obj.firstvalue('999.9', default='X'), 'X')

    def test_get_first_many_values(self):
        obj = marcx.Record()
        for i in range(100):
            obj.add('020', a='isbn-no-%s' % i)
        self.assertEqual(obj.firstvalue('020.a'), 'isbn-no-0')

    def test_remove_field_if(self):
        obj = marcx.Record(data=MARCREC, to_unicode=True, force_utf8=True)

        removed = obj.remove_field_if('689.5', marcx._equals('DE-576'))
        self.assertEqual(len(removed), 1)

        removed = obj.remove_field_if('689.5', marcx._equals('DE-576'))
        self.assertEqual(len(removed), 0)

    def test_remove_field_if_multiple_fields(self):
        obj = marcx.Record()

        # this is one field!
        obj.add('020', a='978123123', z='978123123')
        removed = obj.remove_field_if('020.a', '020.z', marcx._startswith('978'))
        self.assertEqual(len(removed), 1)

        obj = marcx.Record()
        # this is one field!
        obj.add('020', a='978123123', z='978123123')
        removed = obj.remove_field_if('020.a', marcx._startswith('978'))
        self.assertEqual(len(removed), 1)
        # no other field remains
        self.assertEqual(len(obj.get_fields()), 0)

        obj = marcx.Record()
        # these are two fields!
        obj.add('020', a='978123123')
        obj.add('020', z='978123123')
        removed = obj.remove_field_if('020.a', '020.z', marcx._startswith('978'))
        self.assertEqual(len(removed), 2)

        obj = marcx.Record()
        # these are three fields!
        obj.add('020', a='978123123')
        obj.add('020', z='978123123')
        obj.add('776', x='978123123')
        removed = obj.remove_field_if('020.a', '020.z', '776.x', marcx._startswith('978'))
        self.assertEqual(len(removed), 3)

    def test_add_digits_subfields_with_underscore(self):
        obj = marcx.Record()
        obj.add('020', a='978123123', _9='Hello')
        self.assertEqual(
            obj.get_fields('020')[0].get_subfields('9'), ['Hello'])

    def test_test(self):
        def _is_valid_isbn(value):
            ''' poor man's isbn validator '''
            return len(value) in (10, 13)

        obj = marcx.Record()
        # these are three fields!
        obj.add('020', a='9783334444333')
        obj.add('020', a='978000')
        obj.add('020', z='9783330000333')
        obj.add('776', x='978111')

        self.assertTrue(obj.test('020.a', _is_valid_isbn))
        self.assertTrue(obj.test('020.z', '776.x', _is_valid_isbn))

        self.assertFalse(obj.test('020.a', _is_valid_isbn, all=True))
        self.assertFalse(obj.test('776.x', _is_valid_isbn))

    def test_remove(self):
        """ test field or subfield removal """

        obj = marcx.Record()
        obj.add('020', a='9783334444333')
        obj.add('020', a='978000')
        obj.add('020', z='9783330000333')
        obj.add('776', x='978111')

        obj.remove('020.a')
        self.assertEqual(len(obj.get_fields()), 2)

        obj.add('001', data='123')
        self.assertEqual(len(obj.get_fields()), 3)
        obj.remove('001')
        self.assertEqual(len(obj.get_fields()), 2)

        obj.remove('020')
        self.assertEqual(len(obj.get_fields()), 1)

        obj.remove('776.y')
        self.assertEqual(len(obj.get_fields()), 1)

        obj.remove('776.x')
        self.assertEqual(len(obj.get_fields()), 0)

    def test_remove_subfields(self):
        obj = marcx.Record()
        obj.add('020', a='978000', b='123', c='123')
        obj.remove('020.a')
        obj.remove('020.b')
        self.assertEqual(obj.get_fields('020')[0].subfields, [Subfield(code='c', value='123')])
        obj.remove('020.c')
        self.assertEqual(obj.get_fields('020'), [])

    def test_remove_cross_field_subfields(self):
        obj = marcx.Record()
        obj.add('020', a='978000', b='123')
        obj.add('020', b='123', c='123')

        obj.remove('020.a')
        self.assertEqual(obj.get_fields('020')[0].subfields, [Subfield(code='b', value='123')])
        self.assertEqual(sorted(obj.get_fields('020')[1].subfields),
                         [Subfield(code='b', value='123'), Subfield(code='c', value='123')])

        obj.remove('020.b')
        # note that one field disappears, since it no longer carries subfields
        self.assertEqual(obj.get_fields('020')[0].subfields, [Subfield(code='c', value='123')])

        obj.remove('020.c')
        # no more 020 at all
        self.assertEqual(obj.get_fields('020'), [])

    def test_itervalues(self):
        obj = marcx.Record()
        obj.add('020', a='9783334444333')
        obj.add('020', a='978000')
        obj.add('020', z='9783330000333')
        obj.add('776', x='978111')

        self.assertEqual(len(list(obj.itervalues('020.a'))), 2)
        self.assertEqual(len(list(obj.itervalues('020'))), 3)
        self.assertEqual(len(list(obj.itervalues('020', '776'))), 4)
        self.assertEqual(len(list(obj.itervalues('020', '776', '001'))), 4)
        self.assertEqual(len(list(obj.itervalues('001'))), 0)

    def test_from_record(self):
        record = pymarc.Record()
        record.add_field(pymarc.field.Field('001', data='123'))
        record.add_field(pymarc.field.Field('020', [' ', ' '], subfields=L(['a', '123'])))

        with self.assertRaises(AttributeError):
            record.itervalues('020')

        obj = marcx.Record.from_record(record)
        self.assertEqual(obj.__class__.__name__, 'Record')
        self.assertEqual(list(obj.itervalues('020')), ['123'])

    def test_to_record(self):
        obj = marcx.Record()
        obj.add('020', a='9783334444333')
        obj.add('020', a='978000')
        obj.add('020', z='9783330000333')
        obj.add('776', x='978111')
        record = obj.to_record()
        self.assertEqual(len(record.get_fields()), 4)
        self.assertEqual(len(record.get_fields('020')), 3)
        self.assertEqual(record.get_fields('020')[0].value(), '9783334444333')
        self.assertEqual(record.get_fields('020')[1].value(), '978000')
        self.assertEqual(record.get_fields('020')[2].value(), '9783330000333')
        self.assertEqual(record.get_fields('776')[0].value(), '978111')

    def test_add_repeated_subfields(self):
        obj = marcx.Record()
        obj.add('020', a=('9783334444333', '1234'))
        self.assertEqual(len(obj.get_fields()), 1)

    def test_add_fails_on_non_string_non_iterables(self):
        obj = marcx.Record()
        with self.assertRaises(ValueError):
            obj.add('020', a=1243)

    def test_has(self):
        obj = marcx.Record()
        obj.add('020', a='1243')
        self.assertTrue(obj.has('020'))
        self.assertTrue(obj.has('020.a'))
        self.assertFalse(obj.has('020.b'))

    def test_flatten(self):
        obj = marcx.Record()
        obj.add('020', a='1243')
        self.assertEqual(obj.flatten(), ['1243'])
        obj.add('020', b='Hello World')
        self.assertEqual(obj.flatten(), ['1243', 'Hello World'])
        obj.add('020', c='1243')
        self.assertEqual(obj.flatten(), ['1243', 'Hello World', '1243'])

    def test_flatten_order(self):
        """
        Flatten does not guarantee any order.
        """
        obj = marcx.Record()
        obj.add('020', a='1', b='2', c='3', d='4', e='5', f='6')
        self.assertEqual(set(obj.flatten()), set(['1', '2', '3', '4', '5', '6']))

    def test_add_strict_flag(self):
        obj = marcx.Record()
        with self.assertRaises(ValueError):
            obj.add("007", data="")

        obj = marcx.Record()
        obj.strict = False
        obj.add("001", data="")
        obj.add("007", data="")
        self.assertEqual(len(obj.get_fields()), 0)

    def test_add_many_empty_subfields(self):
        obj = marcx.Record()
        obj.strict = True
        with self.assertRaises(ValueError):
            obj.add("245", a="", b="", c="")

        obj = marcx.Record()
        obj.strict = False
        obj.add("245", a="", b="", c="")
        self.assertEqual(len(obj.get_fields()), 0)

        obj = marcx.Record()
        obj.strict = False
        obj.add("245", a="", b="", c="x")
        self.assertEqual(len(obj.get_fields()), 1)

    def test_ordered_subfields_via_kwarg(self):
        obj = marcx.Record()
        obj.add("245", subfields=["a", "Hello", "b", "World", "c", "!"])
        self.assertEqual(len(obj.get_fields()), 1)
        self.assertEqual(len(obj.get_fields("245")), 1)
        self.assertEqual(len(obj.get_fields("245")[0].get_subfields("a")), 1)
        self.assertEqual(len(obj.get_fields("245")[0].get_subfields("b")), 1)
        self.assertEqual(len(obj.get_fields("245")[0].get_subfields("c")), 1)

    def test_ordered_subfields_via_kwarg_empty_values(self):
        obj = marcx.Record()
        obj.strict = True
        obj.add("245", subfields=["a", "x", "b", ""])
        self.assertEqual(len(obj.get_fields()), 1)
        self.assertEqual(len(obj.get_fields()[0].subfields_as_dict()), 1)
        self.assertEqual(len(obj.get_fields()[0].get_subfields("a")), 1)

        obj = marcx.Record()
        obj.strict = True
        with self.assertRaises(ValueError):
            obj.add("245", subfields=["a", "", "b", "", "c", ""])

        obj = marcx.Record()
        obj.strict = False
        obj.add("245", subfields=["a", "", "b", "", "c", ])
        self.assertEqual(len(obj.get_fields()), 0)

    def test_repeated_subfield_empty_value_not_added(self):
        obj = marcx.Record()
        obj.strict = True
        obj.add("245", a=["Hello", "", "X!"])
        self.assertEqual(len(obj.get_fields()), 1)
        print(obj)
        self.assertEqual(len(obj.get_fields()[0].subfields_as_dict()), 1)
