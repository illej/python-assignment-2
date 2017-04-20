from cmd import Cmd
from view import View
import sys


class CmdView(View, Cmd):
    def __init__(self):
        super(View, self).__init__()
        self.intro = "Welcome.\n-- Type 'help' for a list of commands."
        self.prompt = "> "
        self.__controller = None

    def help_cmd(self):
        print('Syntax: python main.py [flag] .. (up to 5) [data] .. (up to 3)')
        print('\n\t:args: Used to invoke functionality from the command-line.')
        print('\t-r\t\tRebuild the database')
        print('\t-g\t\tRead files from cwd')
        print('\t-v\t\tValidate data')
        print('\t-c\t\tCommit valid data to database')
        print('\t-d [data]*\tDisplay default chart (bar chart). Can be called if database is not empty.')
        print('\t\t\t\t* up to 3 sets')
        print('\n\t\tNOTE: -r, -g, -v, -c, must be used in order.')

    def _initialise(self):
        for arg in sys.argv:
            if arg == '-r':
                self.do_rebuild_db('')
            elif arg == '-g':
                self.do_get('')
            elif arg == '-v':
                self.do_validate('')
            elif arg == '-c':
                self.do_commit('')
            elif arg == '-d':
                data_index = sys.argv.index(arg) + 1
                args_list = sys.argv[data_index:]
                formatted_str = ('{} ' * len(args_list)).format(*args_list)
                self.do_display('-b ' + formatted_str)

    def set_controller(self, controller):
        self.__controller = controller
        self._initialise()

    def do_quit(self, line):
        """
        Syntax: quit
            -> Closes the program.

        :param: None
        :return: None
        """
        return True

    def do_validate(self, line):
        """
        Syntax: validate
            -> Checks the validity of previously read data before committing it to the database.

        :param: None
        :return: None
        """
        self.__controller.validate()

    def do_commit(self, line):
        """
        Syntax: commit
            -> Commits valid data to the database to be stored.

        :param: None
        :return: None
        """
        self.__controller.commit()

    def do_get(self, line):
        """
        Syntax: get [line]
            -> Reads and processes data from .txt file(s).

        :param [line]: Optional
            none        If no command is specified, then files in the cwd are read.
            cwd         Shows the current working directory, and lists sub-folders.
            <folder>    Changes the cwd to the specified sub-folder, and reads any .txt files.
        """
        try:
            self.get(line)
        except Exception as e:
            print('cmd:', e)

    def get(self, line):
        self.__controller.get(line)

    def set(self, **kwargs):
        # TODO: print data to console as a table?
        pass

    def do_display(self, line):
        """
        Syntax: display [flag] [data] [data] .. (up to 3)
            -> Displays a chart comparing data sets.

        :param [flag]: Display chart/graph type.
            -p          Pie chart
            -b          Bar chart
            -l          Line graph
            -r          Radar chart
        :param [data]: Data set to be displayed.
            age         Age of employee
            salary      Salary of employee
            sales       Sales of employee
        """
        self.__controller.display(line)

    def do_query(self, line):
        """
        Syntax: query [line]
            -> Returns basic data from the database.

        :param [line]:
            *           Retrieves all data
            id          Retrieves all empids
            age         Retrieves all ages
            gender      Retrieves all genders
            salary      Retrieves all salaries
            bmi         Retrieves all body mass indexes
            birthday    Retrieves all birthday
        """
        self.__controller.get(line)

    def do_rebuild_db(self, line):
        """
        Syntax: rebuild_db
            -> Wipes all current data from the database and rebuilds it.
                * May need to restart application to take effect.

        :param: None
        :return: None
        """
        self.__controller.rebuild_db()

    def do_serialize(self, line):
        """
        Syntax: serialize [filename]
            OR  serialize [flag] [filename]

            -> Writes the current database information to a serialized pickle file.
            OR -> Opens the specifies pickle file and displays its contents.

        :param [filename]: Filename for the pickle file to store database data.
        :param [flag]:
            -r      Read from file instead of write.
        """
        self.__controller.serialize(line)

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
