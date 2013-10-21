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
            "a": "Part 1 Introduction: What is metadata? Part 2 Implementation of metadata creation activities: Choosing metadata for a digital library project-- Creating metadata usage guidelines-- Creating metadata-- Practical implementation of a metadata strategy Part 3 Systems design: Functions performed by a digital library system-- Metadata that drives discovery functionality. Part 4 Metadata interoperability: Defining interoperability-- Interoperability and resource discovery-- Technical interoperability-- Content interoperability: shareable metadata. Part 5 Conclusion: The future of metadata.",
            "ind1": "0",
            "ind2": " "
         }
      ],
      "520": [
         {
            "a": "This book assists information professionals in improving the usability of digital objects by adequately documenting them and using tools for metadata management. It provides practical advice for libraries, archives, and museums dealing with digital collections in a wide variety of formats and from a wider variety of sources.",
            "b": "This book assists information professionals in improving the usability of digital objects by adequately documenting them and using tools for metadata management. It provides practical advice for libraries, archives, and museums dealing with digital collections in a wide variety of formats and from a wider variety of sources. This book is forward-thinking in its approach to using metadata to drive digital library systems, and will be a valuable resource for those creating and managing digital resources as technologies for using those resources grow and change.",
            "ind1": " ",
            "ind2": " "
         }
      ],
      "545": [
         {
            "a": "Muriel Foulonneau is project coordinator at the University of Illinois at Urbana-Champaign for the CIC-OAI metadata harvesting project. She has served as an evaluator for the Information Science and Technology R&D program of the European Commission. Jenn Riley is the Metadata Librarian for the Indiana University Digital Library Program, where she is responsible for planning metadata strategy for digital library projects. They have both been involved in the definition of best practices for shareable metadata for the Digital Library Federation. They have authored numerous practical guides and research articles on interoperability of digital content.",
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
   "original": "03849cam a22004212a 4500001001400000003000800014005001700022007000300039008004100042020003600083020003300119040002600152072001600178072001600194072001500210082001400225100001700239245012400256260014100380300003400521365009000555365011800645365009200763366006900855366003900924366006600963500001401029505059401043520089801637545066002535650001403195650002603209650005003235650005503285650002903340650003403369700002403403\u001e9781843343028\u001eUK-WkNB\u001e20130521000000.0\u001eta\u001e060721e200803uuxxka   | |||||||0|0 eng|d\u001e  \u001fa9781843343028 (hbk.) :\u001fc£59.95\u001e  \u001fa1843343029 (hbk.) :\u001fc£59.95\u001e  \u001faUK-WkNB\u001fbeng\u001fcUK-WkNB\u001e 7\u001faGLC\u001f2bicssc\u001e 7\u001faUMW\u001f2bicssc\u001e 7\u001faLIB\u001f2eflch\u001e04\u001fa025.3\u001f222\u001e1 \u001faRiley, Jenn.\u001e10\u001faMetadata for digital resources :\u001fbImplementation, systems design and interoperability /\u001fcJenn Riley, Muriel Foulonneau.\u001e  \u001faWitney :\u001fbChandos Publishing (Oxford) Ltd :\u001fb[distributor] Woodhead Publishing Ltd :\u001fb[distributor] American Library Association,\u001fc2008.\u001e  \u001fa220 p. :\u001fbill. ;\u001fc23x16x1 cm.\u001e  \u001fa02\u001fb59.95\u001fcGBP\u001fd00\u001fhZ 59.95 0.0 59.95 0.00\u001fjGB\u001fkxxk\u001fmWoodhead Publishing Ltd\u001f2onix-pt\u001e  \u001fa02\u001fb100.00\u001fcUSD\u001fd00\u001feLocal taxes may apply\u001fhZ 100.00 0.0 100.00 0.00\u001fjUS\u001fkxxu\u001fmIngram Publisher Services\u001f2onix-pt\u001e  \u001fa02\u001fb118.95\u001fcAUD\u001fd00\u001fhS 108.14 10.0 118.95 10.81\u001fjAU\u001fkat\u001fmCentral Book Services\u001f2onix-pt\u001e  \u001fb20080301\u001fcIP 20090213\u001fjGB\u001fkxxk\u001fmLightning Source UK Ltd\u001f2UK-WkNB\u001e  \u001fb20080301\u001fjUS\u001fkxxu\u001fmIngram\u001f2UK-WkNB\u001e  \u001fb20071027\u001fcIP 20090708\u001fjAU\u001fkat\u001fmCentral Book Services\u001f2UK-WkNB\u001e  \u001faHardback.\u001e0 \u001faPart 1 Introduction: What is metadata? Part 2 Implementation of metadata creation activities: Choosing metadata for a digital library project-- Creating metadata usage guidelines-- Creating metadata-- Practical implementation of a metadata strategy Part 3 Systems design: Functions performed by a digital library system-- Metadata that drives discovery functionality. Part 4 Metadata interoperability: Defining interoperability-- Interoperability and resource discovery-- Technical interoperability-- Content interoperability: shareable metadata. Part 5 Conclusion: The future of metadata.\u001e  \u001faThis book assists information professionals in improving the usability of digital objects by adequately documenting them and using tools for metadata management. It provides practical advice for libraries, archives, and museums dealing with digital collections in a wide variety of formats and from a wider variety of sources.\u001fbThis book assists information professionals in improving the usability of digital objects by adequately documenting them and using tools for metadata management. It provides practical advice for libraries, archives, and museums dealing with digital collections in a wide variety of formats and from a wider variety of sources. This book is forward-thinking in its approach to using metadata to drive digital library systems, and will be a valuable resource for those creating and managing digital resources as technologies for using those resources grow and change.\u001e0 \u001faMuriel Foulonneau is project coordinator at the University of Illinois at Urbana-Champaign for the CIC-OAI metadata harvesting project. She has served as an evaluator for the Information Science and Technology R&D program of the European Commission. Jenn Riley is the Metadata Librarian for the Indiana University Digital Library Program, where she is responsible for planning metadata strategy for digital library projects. They have both been involved in the definition of best practices for shareable metadata for the Digital Library Federation. They have authored numerous practical guides and research articles on interoperability of digital content.\u001e 0\u001faMetadata.\u001e 0\u001faMetadata\u001fxManagement.\u001e 0\u001faElectronic information resources\u001fxManagement.\u001e 7\u001faLibrary, archive & information management.\u001f2bicssc\u001e 7\u001faWeb programming.\u001f2bicssc\u001e 7\u001faLibraries and Museums.\u001f2eflch\u001e1 \u001faFoulonneau, Muriel.\u001e\u001d",
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