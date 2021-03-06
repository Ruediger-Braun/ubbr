
from unittest import TestCase
from ubbr.engine.core import Ubbr

import os


import json


class UbbrTest(TestCase):


    def setUp(self):
        fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'fixtures')
        with open(os.path.join(fixtures_path,'testcases.json')) as tc_file:
            self.testcases = json.load(tc_file)




    def test_make_method(self):
        cases = [a for a in self.testcases if a['test'].startswith('basic')]
        for tc in cases:
            u = Ubbr(tc['source'])
            op = u._make()
            self.assertEqual(op[0],tc['output']['template'])
            self.assertEqual(op[1],tc['output']['code_fragments'])

    def test_get_context(self):
        cases = [a for a in self.testcases if a['test'].startswith('basic')]
        for tc in cases:
            u = Ubbr(tc['source'])
            nodes = u.get_context()[0]
            self.assertEqual(nodes,tc['output']['ubbrvalues'])

   
    def test_random_seed(self):
        #  checking that the random seed passes to the Ubbr correctly
        cases = [a for a in self.testcases if a['test'].startswith('random')]
        for tc in cases:
            u = Ubbr(tc['source'])
            one = u.get_context(random_seed=4)
            two = u.get_context(random_seed=4)
            self.assertEqual(one,two)

    def test_string_input(self):
        cases = [case for case in self.testcases if case['test']=='input']
        for tc in cases:
            u = Ubbr(tc['source'])
            nodes = u.get_context()[0]
            for j in range(len(nodes)):
                self.assertRegex(nodes[j],tc['output']['ubbrvalues'][j])

    def test_xml_style_tags(self):
        cases = [case for case in self.testcases if case['test']=='xml tags']
        for tc in cases:
            u = Ubbr(tc['source'],tag_style='xml')
            ubbrvalues = u.get_context()[0]
            self.assertEqual(ubbrvalues,tc['output']['ubbrvalues'])


