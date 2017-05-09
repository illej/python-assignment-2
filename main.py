from controller import Controller
from cmdview import CmdView
from file_reader import FileReader
from dataparser import DataParser
from validator import Validator
from database import Database
from visualiser import Visualiser
from serializer import Serializer

if __name__ == "__main__":
    parser = DataParser()
    cmd_view = CmdView()
    file_reader = FileReader()
    validator = Validator()
    db = Database("test.db")
    vis = Visualiser()
    serial = Serializer()

    con = Controller(cmd_view, file_reader, parser, validator, db, vis, serial)
    cmd_view.set_controller(con)

    # run program
    cmd_view.cmdloop()
