from controller import Controller
from cmdview import CmdView
from fileview import FileView
from dataparser import DataParser
from validator import Validator
from databaseview import DatabaseView
from visualiser import Visualiser

if __name__ == "__main__":
    parser = DataParser()
    cmd_view = CmdView()
    file_view = FileView()
    validator = Validator()
    db = DatabaseView("test.db")
    vis = Visualiser()

    con = Controller(cmd_view, file_view, parser, validator, db, vis)
    cmd_view.set_controller(con)

    # run program
    cmd_view.cmdloop()
