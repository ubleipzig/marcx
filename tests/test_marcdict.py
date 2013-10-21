#!/usr/bin/env python
# coding: utf-8

EXAMPLE = """
{
   "content": {
      "100": [
         {
            "a": "Riley, Jenn.",
            "ind1": "1",
            "ind2": " "
         }
      ],
      "245": [
         {
            "a": "Metadata for digital resources :",
            "c": "Jenn Riley, Muriel Foulonneau.",
            "b": "Implementation, systems design and interoperability /",
            "ind1": "1",
            "ind2": "0"
         }
      ],
      "260": [
         {
            "a": "Witney :",
            "c": "2008.",
            "b": "[distributor] American Library Association,",
            "ind1": " ",
            "ind2": " "
         }
      ],
      "300": [
         {
            "a": "220 p. :",
            "c": "23x16x1 cm.",
            "b": "ill. ;",
            "ind1": " ",
            "ind2": " "
         }
      ],
      "365": [
         {
            "2": "onix-pt",
            "a": "02",
            "c": "GBP",
            "b": "59.95",
            "ind1": " ",
            "d": "00",
            "ind2": " ",
            "h": "Z 59.95 0.0 59.95 0.00",
            "k": "xxk",
            "j": "GB",
            "m": "Woodhead Publishing Ltd"
         },
         {
            "2": "onix-pt",
            "a": "02",
            "c": "USD",
            "b": "100.00",
            "e": "Local taxes may apply",
            "d": "00",
            "ind2": " ",
            "h": "Z 100.00 0.0 100.00 0.00",
            "k": "xxu",
            "j": "US",
            "m": "Ingram Publisher Services",
            "ind1": " "
         },
         {
            "2": "onix-pt",
            "a": "02",
            "c": "AUD",
            "b": "118.95",
            "ind1": " ",
            "d": "00",
            "ind2": " ",
            "h": "S 108.14 10.0 118.95 10.81",
            "k": "at",
            "j": "AU",
            "m": "Central Book Services"
         }
      ],
      "366": [
         {
            "2": "UK-WkNB",
            "c": "IP 20090213",
            "b": "20080301",
            "ind1": " ",
            "ind2": " ",
            "k": "xxk",
            "j": "GB",
            "m": "Lightning Source UK Ltd"
         },
         {
            "2": "UK-WkNB",
            "b": "20080301",
            "ind1": " ",
            "ind2": " ",
            "k": "xxu",
            "j": "US",
            "m": "Ingram"
         },
         {
            "2": "UK-WkNB",
            "c": "IP 20090708",
            "b": "20071027",
            "ind1": " ",
            "ind2": " ",
            "k": "at",
            "j": "AU",
            "m": "Central Book Services"
         }
      ],
      "500": [
         {
            "a": "Hardback.",
            "ind1": " ",
            "ind2": " "
         }
      ],
      "505": [
         {
            "a": "Part 1 Introduction: What is metadata? Part 2 ",
            "ind1": "0",
            "ind2": " "
         }
      ],
      "520": [
         {
            "a": "This book assists information professionals in ",
            "b": "This book assists information professionals in ",
            "ind1": " ",
            "ind2": " "
         }
      ],
      "545": [
         {
            "a": "Muriel Foulonneau is project coordinator at the",
            "ind1": "0",
            "ind2": " "
         }
      ],
      "650": [
         {
            "a": "Metadata.",
            "ind1": " ",
            "ind2": "0"
         },
         {
            "a": "Metadata",
            "x": "Management.",
            "ind1": " ",
            "ind2": "0"
         },
         {
            "a": "Electronic information resources",
            "x": "Management.",
            "ind1": " ",
            "ind2": "0"
         },
         {
            "2": "bicssc",
            "a": "Library, archive & information management.",
            "ind1": " ",
            "ind2": "7"
         },
         {
            "2": "bicssc",
            "a": "Web programming.",
            "ind1": " ",
            "ind2": "7"
         },
         {
            "2": "eflch",
            "a": "Libraries and Museums.",
            "ind1": " ",
            "ind2": "7"
         }
      ],
      "700": [
         {
            "a": "Foulonneau, Muriel.",
            "ind1": "1",
            "ind2": " "
         }
      ],
      "072": [
         {
            "2": "bicssc",
            "a": "GLC",
            "ind1": " ",
            "ind2": "7"
         },
         {
            "2": "bicssc",
            "a": "UMW",
            "ind1": " ",
            "ind2": "7"
         },
         {
            "2": "eflch",
            "a": "LIB",
            "ind1": " ",
            "ind2": "7"
         }
      ],
      "leader": {
         "status": "c",
         "subfieldcodelength": 2,
         "entrymap": "4500",
         "impldef1": "m ",
         "codingschema": "a",
         "raw": "03849cam a22004212a 4500",
         "length": 3849,
         "indicatorcount": 2,
         "type": "a",
         "impldef2": "2a "
      },
      "082": [
         {
            "2": "22",
            "a": "025.3",
            "ind1": "0",
            "ind2": "4"
         }
      ],
      "001": "9781843343028",
      "007": "ta",
      "020": [
         {
            "a": "9781843343028 (hbk.) :",
            "c": "£59.95",
            "ind1": " ",
            "ind2": " "
         },
         {
            "a": "1843343029 (hbk.) :",
            "c": "£59.95",
            "ind1": " ",
            "ind2": " "
         }
      ],
      "005": "20130521000000.0",
      "008": "060721e200803uuxxka   | |||||||0|0 eng|d",
      "040": [
         {
            "a": "UK-WkNB",
            "c": "UK-WkNB",
            "b": "eng",
            "ind1": " ",
            "ind2": " "
         }
      ],
      "003": "UK-WkNB"
   },
   "sha1": "316a18d70e8310263b7b1780a7b08b87d29870af",
   "meta": {
      "date": "2013-10-16",
      "ptag": "10111010"
   },
   "original": "03849cam a22004212a 4500001001400000003",
   "content_type": "application/marc"
}
"""

import marcx
import pymarc
import json
import unittest

class MarcDictTests(unittest.TestCase):

    def test_init(self):
        r = marcx.marcdict()
        self.assertIsNotNone(r)

    def test_marcdict_behaves_like_a_dict(self):
        d = json.loads(EXAMPLE)
        r = marcx.marcdict(d)
        self.assertEquals(5, len(r.values()))
        self.assertTrue('content' in r.keys())
        self.assertTrue('content_type' in r.keys())
        self.assertTrue('meta' in r.keys())
        self.assertTrue('original' in r.keys())
        self.assertTrue('sha1' in r.keys())

    def test_marcdict_access(self):
        d = json.loads(EXAMPLE)
        r = marcx.marcdict(d)
        self.assertEquals(['316a18d70e8310263b7b1780a7b08b87d29870af'],
                          r.values('sha1'))
        self.assertEquals(['2013-10-16'], r.values('meta.date'))
        self.assertEquals(['9781843343028 (hbk.) :', '1843343029 (hbk.) :'],
                          r.values('content.020.a'))
        self.assertEquals(['a'],
                  r.values('content.leader.codingschema'))
        self.assertEquals(['bicssc', 'bicssc', 'eflch'],
                  r.values('content.072.2'))
        self.assertEquals(['Witney :', '2008.', '[distributor] American Library Association,', ' ', ' '],
          r.values('content.260'))

    def test_marcdict_firstvalue(self):
        d = json.loads(EXAMPLE)
        r = marcx.marcdict(d)
        self.assertEquals('2013-10-16', r.firstvalue('meta.date'))
        self.assertEquals('9781843343028 (hbk.) :', r.firstvalue('content.020.a'))
        self.assertEquals('bicssc', r.firstvalue('content.072.2'))
        self.assertEquals(None, r.firstvalue('content.072.ZZZ'))

