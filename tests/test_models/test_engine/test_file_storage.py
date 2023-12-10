#!/usr/bin/python3
""" this Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import pep8
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """ the Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_style_check(self):
        """
        Tests pep8 style
        """
        style = pep8.StyleGuide(quiet=True)
        pep_chk = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(pep_chk.total_errors, 0, "fix pep8")

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        bsmdl = BaseModel()
        usr = User()
        ste = State()
        plc = Place()
        cty = City()
        amty = Amenity()
        rvw = Review()
        models.storage.new(bsmdl)
        models.storage.new(usr)
        models.storage.new(ste)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amty)
        models.storage.new(rvw)
        self.assertIn("BaseModel." + bsmdl.id, models.storage.all().keys())
        self.assertIn(bsmdl, models.storage.all().values())
        self.assertIn("User." + usr.id, models.storage.all().keys())
        self.assertIn(usr, models.storage.all().values())
        self.assertIn("State." + ste.id, models.storage.all().keys())
        self.assertIn(ste, models.storage.all().values())
        self.assertIn("Place." + plc.id, models.storage.all().keys())
        self.assertIn(plc, models.storage.all().values())
        self.assertIn("City." + cty.id, models.storage.all().keys())
        self.assertIn(cty, models.storage.all().values())
        self.assertIn("Amenity." + amty.id, models.storage.all().keys())
        self.assertIn(amty, models.storage.all().values())
        self.assertIn("Review." + rvw.id, models.storage.all().keys())
        self.assertIn(rvw, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        bsmdl = BaseModel()
        usr = User()
        ste = State()
        plc = Place()
        cty = City()
        amty = Amenity()
        rvw = Review()
        models.storage.new(bsmdl)
        models.storage.new(usr)
        models.storage.new(ste)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amty)
        models.storage.new(rvw)
        models.storage.save()
        sv_txt = ""
        with open("file.json", "r") as f:
            sv_txt = f.read()
            self.assertIn("BaseModel." + bsmdl.id, sv_txt)
            self.assertIn("User." + usr.id, sv_txt)
            self.assertIn("State." + ste.id, sv_txt)
            self.assertIn("Place." + plc.id, sv_txt)
            self.assertIn("City." + cty.id, sv_txt)
            self.assertIn("Amenity." + amty.id, sv_txt)
            self.assertIn("Review." + rvw.id, sv_txt)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        """
        this Tests method: reload (reloads objects from string file)
        """
        a_strg = FileStorage()
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        with open("file.json", "w") as f:
            f.write("{}")
        with open("file.json", "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(a_strg.reload(), None)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()

