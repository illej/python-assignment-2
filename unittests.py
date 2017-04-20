import unittest
from controller import Controller
from cmdview import CmdView
from fileview import FileView
from dataparser import DataParser
from validator import Validator
from databaseview import DatabaseView
from visualiser import Visualiser


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.parser = DataParser()
        self.cmd_view = CmdView()
        self.file_view = FileView()
        self.validator = Validator()
        self.db = DatabaseView("test.db")
        self.vis = Visualiser()
        # self.val = Validator()
        self.controller = Controller(self.cmd_view, self.file_view, self.parser, self.validator, self.db, self.vis)

    def tearDown(self):
        pass

    def test_01_parser_to_list(self):
        expected = ['empid=D011', 'gender=M', 'age=29']
        actual = DataParser()._to_list("empid=D011\ngender=M\nage=29")
        self.assertEqual(expected, actual)

    def test_02_parser_to_dict(self):
        expected = {'empid': 'D011', 'gender': 'M', 'age': '29'}
        actual = DataParser()._to_dict(['empid=D011', 'gender=M', 'age=29'])
        self.assertEqual(expected, actual)

    def test_03_parser_scrub_db_list(self):
        expected = [14, 25]
        actual = DataParser().scrub_db_list([(14,), (25,)])
        self.assertEqual(expected, actual)

    @unittest.skip("unfinished test case")
    def test_04_validator_validate(self):
        self.validator.validate({'empid': 'D011', 'gender': 'M'})
        expected = [{'empid': 'D011', 'gender': 'M'}]
        actual = self.validator.get_valid_sets()
        self.assertEqual(expected, actual)

    @unittest.skip("unfinished test case")
    def test_05_controller_serialize(self):
        self.controller.serialize('poop')
        self.controller.serialize('-r poop')
        expected = ('D012', 'M', 29, 722, 'Normal', 320, '23-11-1987')
        actual = self.controller.serialize('-r poop')
        self.assertEqual(expected, actual)

    # only works with data from root of main.py
    def test_06_db_query(self):
        expected = [(29,), (22,), (35,), (29,), (30,), (22,), (21,), (50,), (52,), (19,), (38,), (35,), (29,)]
        actual = self.db.get('age')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main(verbosity=True)
