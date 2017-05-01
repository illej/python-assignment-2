import unittest
import io
import sys
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
        self.val = Validator()
        self.controller = Controller(self.cmd_view,
                                     self.file_view,
                                     self.parser,
                                     self.validator,
                                     self.db,
                                     self.vis)
        self.init()

    def tearDown(self):
        self.parser = None
        self.cmd_view = None
        self.file_view = None
        self.validator = None
        self.db = None
        self.vis = None
        self.val = None
        self.controller = None

    def init(self):
        sys.stdout = io.StringIO()
        self.db.rebuild()
        self.controller.get('')
        self.controller.validate()
        self.controller.commit()
        sys.stdout = sys.__stdout__

    # DataParser
    def test_01_parser_to_list(self):
        expected = ['empid=D011', 'gender=M', 'age=29']
        actual = self.parser._to_list("empid=D011\ngender=M\nage=29")
        self.assertEqual(expected, actual)

    def test_02_parser_to_dict(self):
        expected = {'empid': 'D011', 'gender': 'M', 'age': '29'}
        actual = self.parser._to_dict(['empid=D011', 'gender=M', 'age=29'])
        self.assertEqual(expected, actual)

    def test_03_parser_scrub_db_list(self):
        expected = [14, 25]
        actual = self.parser.scrub_db_list([(14,), (25,)])
        self.assertEqual(expected, actual)

    def test_04_parser_parse_raw_data(self):
        input = "empid=D011\ngender=M\nage=29"
        parser = DataParser()
        parser.parse_raw_data(input)

        expected = [{'empid': 'D011', 'gender': 'M', 'age': '29'}]
        actual = parser.get_data()
        self.assertEqual(expected, actual)

    # Controller.serialize()
    def test_05_controller_serialize_write(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.serialize('socks')

        expected = '-- Database pickled!\n\t-> as filename: socks.pickle.\n'
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_06_controller_serialize_empty_db(self):
        captured_prep = io.StringIO()
        sys.stdout = captured_prep
        self.controller.rebuild_db()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.serialize('poop')

        expected = '* Database is empty. Nothing to serialize.\n'
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_07_controller_serialize_read(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.serialize('-r socks')

        expected = "('D011', 'M', 29, 722, 'Normal', 320, '23-11-1987')\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_08_controller_serialize_invalid_params(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.serialize('poop socks')

        expected = "* Invalid parameters.\n-- Type 'help serialize' for more details.\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_09_controller_serialize_no_file(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.serialize('-r poopie')

        expected = "[Errno 2] No such file or directory: 'poopie.pickle'\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    # Controller.validate()
    def test_10_controller_validate_fail(self):
        self.controller = Controller(self.cmd_view,
                                     self.file_view,
                                     DataParser(),
                                     self.validator,
                                     self.db,
                                     self.vis)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.validate()

        expected = "* No data has been read.\n-- Type 'help get' for more details.\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    # Controller.commit()
    def test_11_controller_commit_fail(self):
        self.controller = Controller(self.cmd_view,
                                     self.file_view,
                                     self.parser,
                                     Validator(),
                                     self.db,
                                     self.vis)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.commit()

        expected = "* No valid data has been entered.\n" \
                   "-- Type 'help validate' for more details.\n" \
                   "'NoneType' object is not iterable\n" \
                   "* Could not commit data to the database.\n" \
                   "-- Type 'help commit' for more details.\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    # Controller.get()
    def test_12_controller_get_fail(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.get('get poopie')

        expected = ''
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    # Controller.query()
    def test_13_controller_query(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.query('*')

        expected = "[('D011', 'M', 29, 722, 'Normal', 320, '23-11-1987')]\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_14_controller_display_no_param(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.display('')

        expected = "* Missing parameters. \n-- Type 'help display' for information on how to use this command.\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_15_controller_display_invalid_input(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.display('poopie')

        expected = "* Invalid input. \n-- Type 'help display' for information on how to use this command.\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_16_controller_display_b(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.display('-b age')

        regex = '^file://C:/Users/Elliot/AppData/Local/Temp/.*$'
        text = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertRegex(text, regex)

    def test_17_controller_display_l(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.display('-l age')

        regex = '^file://C:/Users/Elliot/AppData/Local/Temp/.*$'
        text = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertRegex(text, regex)

    def test_18_controller_display_p(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.display('-p age')

        regex = '^file://C:/Users/Elliot/AppData/Local/Temp/.*$'
        text = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertRegex(text, regex)

    def test_19_controller_display_r(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.display('-r age')

        regex = '^file://C:/Users/Elliot/AppData/Local/Temp/.*$'
        text = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertRegex(text, regex)

    def test_20_controller_display_invalid_falg(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.display('-x age')

        expected = "-- Invalid flag.\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_21_controller_display_invalid_data(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.controller.display('-b poopie')

        expected = "-- Invalid data.\n"
        actual = captured_output.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main(verbosity=True)
