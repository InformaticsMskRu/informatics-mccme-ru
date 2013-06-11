import unittest
import xml
import xml.dom.minidom
#import transaction

#from pyramid import testing

from pynformatics.utils.run import get_protocol_from_file

class TestMyView(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_it(self):
        res = get_protocol_from_file('/home/judges/001594/var/archive/xmlreports/2/S/L/094884')
        dom = xml.dom.minidom.parseString(str(res))
        #self.assertEqual(info['one'].name, 'one')
        #self.assertEqual(info['project'], 'Pynformatics')

if __name__ == '__main__':
    unittest.main()