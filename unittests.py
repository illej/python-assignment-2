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
from view import View
from serializer import Serializer


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.parser = DataParser()
        self.cmd_view = CmdView()
        self.file_view = FileView()
        self.validator = Validator()
        self.db = DatabaseView("test.db")
        self.vis = Visualiser()
        self.val = Validator()
        self.serial = Serializer()
        self.controller = Controller(self.cmd_view,
                                     self.file_view,
                                     self.parser,
                                     self.validator,
                                     self.db,
                                     self.vis,
                                     self.serial)
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
        self.serial = None

    def init(self):
        sys.stdout = io.StringIO()
        self.db.rebuild()
        self.controller.get('')
        self.controller.validate()
        self.controller.commit()
        sys.stdout = sys.__stdout__

    def concreter(self, abclass): # pragma: no cover
        # """
        # >>> import abc
        # >>> class Abstract(metaclass=abc.ABCMeta):
        # ...     @abc.abstractmethod
        # ...     def bar(self):
        # ...        return None
        #
        # >>> c = concreter(Abstract)
        # >>> c.__name__
        # 'dummy_concrete_Abstract'
        # >>> c().bar() # doctest: +ELLIPSIS
        # (<abc_utils.Abstract object at 0x...>, (), {})
        # """
        if not "__abstractmethods__" in abclass.__dict__:
            return abclass
        new_dict = abclass.__dict__.copy()
        for abstractmethod in abclass.__abstractmethods__:
            # replace each abc method or property with an identity function:
            new_dict[abstractmethod] = lambda x, *args, **kw: (x, args, kw)
        # creates a new class, with the overriden ABCs:
        return type("dummy_concrete_%s" % abclass.__name__, (abclass,), new_dict)

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
                                     self.vis,
                                     self.serial)
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
                                     self.vis,
                                     self.serial)
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

    # FileView
    def test_22_fileview_get_cwd(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.controller.get('test-data')
        self.controller.get('cwd')

        expected = "D:\pr301_workspace\\assignment-2\\test-data\n" \
                   "D:\pr301_workspace\\assignment-2\\test-data\n" \
                   "test-folder\n"
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_23_fileview_get_filelist(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.controller.get('')

        expected = "['data.txt', 'data2.txt', 'data3.txt', 'datalist.txt', 'file.txt']\n"
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_24_fileview_get_cd_fail(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.controller.get('poopsickles')

        expected = "fview: [WinError 2] The system cannot find the file specified: './poopsickles'\n"
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    # def test_25_fileview_set(self):
    #     self.file_view.set()

    # not working!
    def test_26_databaseview_initiase_fail(self):
        sys.stdout = io.StringIO()

        self.controller.get('..')

        captured = io.StringIO()
        sys.stdout = captured

        DatabaseView(1)

        expected = 'argument 1 must be str, not int\n'
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_27_databaseview_set_fail(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.db.set(['hi', 'poop', 'socks'])

        expected = ''
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_28_databaseview_get_fail(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.db.get('pickles')

        expected = 'no such column: pickles\n'
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_29_view(self):
        c = self.concreter(View)
        expected = 'dummy_concrete_View'
        actual = c.__name__

        self.assertEqual(expected, actual)

    def test_30_view_get(self):
        View.__abstractmethods__ = set()

        self.assertRaises(NotImplementedError, View().get, 'socks')

    def test_31_view_set(self):
        View.__abstractmethods__ = set()

        self.assertRaises(NotImplementedError, View().set, 'pants')

    # CmdView
    def test_32_cmdview_init_get(self):
        captured = io.StringIO()
        sys.stdout = captured

        sys.argv = ['-g']
        self.cmd_view.set_controller(self.controller)

        expected = "['file.txt']\n"
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_33_cmdview_init_rebuild(self):
        captured = io.StringIO()
        sys.stdout = captured

        sys.argv = ['-r']
        self.cmd_view.set_controller(self.controller)

        expected = '-- db dropped\n-- db rebuit\n'
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_34_cmdview_init_validate(self):
        captured = io.StringIO()
        sys.stdout = captured

        sys.argv = ['-v']
        self.cmd_view.set_controller(self.controller)

        expected = '-- Data validation successful!\n'
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_35_cmdview_init_commit(self):
        captured = io.StringIO()
        sys.stdout = captured

        sys.argv = ['-c']
        self.cmd_view.set_controller(self.controller)

        expected = ''
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_36_cmdview_init_display(self):
        captured = io.StringIO()
        sys.stdout = captured

        sys.argv = ['-d', 'sales']
        self.cmd_view.set_controller(self.controller)

        regex = '^file://C:/Users/Elliot/AppData/Local/Temp/.*$'
        text = captured.getvalue()

        sys.argv = set()
        sys.stdout = sys.__stdout__
        self.assertRegex(text, regex)

    def test_37_cmdview_do_get(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.cmd_view.do_get('pickle-pee')

        expected = "cmd: 'NoneType' object has no attribute 'get'\n"
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    # def test_38_cmdview_set(self):
    #     self.cmd_view.set()

    def test_39_cmdview_quit(self):
        self.cmd_view.do_quit('')

    def test_40_cmdview_query(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.cmd_view.set_controller(self.controller)
        self.cmd_view.do_query('*')

        expected = "[('D011', 'M', 29, 722, 'Normal', 320, '23-11-1987')]\n"
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_41_cmdview_serial(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.cmd_view.set_controller(self.controller)
        self.cmd_view.do_serialize('puppies')

        expected = "-- Database pickled!\n\t-> as filename: puppies.pickle.\n"
        actual = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertEqual(expected, actual)

    def test_42_cmdview_help(self):
        captured = io.StringIO()
        sys.stdout = captured

        self.cmd_view.help_cmd()

        regex = 'Syntax: python main.py'
        text = captured.getvalue()

        sys.stdout = sys.__stdout__
        self.assertRegex(text, regex)

if __name__ == '__main__':  # pragma: no cover
    unittest.main(verbosity=True)
