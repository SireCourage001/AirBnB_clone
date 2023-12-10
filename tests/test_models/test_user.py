#!/usr/bin/python3
"""Defines unittests for models/user.py.
Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        usr_inst_1 = User()
        usr_inst_2 = User()
        self.assertNotEqual(usr_inst_1.id, usr_inst_2.id)

    def test_two_users_different_created_at(self):
        usr_inst_1 = User()
        sleep(0.05)
        usr_inst_2 = User()
        self.assertLess(usr_inst_1.created_at, usr_inst_2.created_at)

    def test_two_users_different_updated_at(self):
        usr_inst_1 = User()
        sleep(0.05)
        usr_inst_2 = User()
        self.assertLess(usr_inst_1.updated_at, usr_inst_2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        main_usr = User()
        main_usr.id = "123456"
        main_usr.created_at = main_usr.updated_at = dt
        usstr = main_usr.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dt_repr, usstr)
        self.assertIn("'updated_at': " + dt_repr, usstr)

    def test_args_unused(self):
        main_usr = User(None)
        self.assertNotIn(None, main_usr.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        main_usr = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(main_usr.id, "345")
        self.assertEqual(main_usr.created_at, dt)
        self.assertEqual(main_usr.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save method of the  class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        main_usr = User()
        sleep(0.05)
        first_updated_at = main_usr.updated_at
        main_usr.save()
        self.assertLess(first_updated_at, main_usr.updated_at)

    def test_two_saves(self):
        main_usr = User()
        sleep(0.05)
        first_updated_at = main_usr.updated_at
        main_usr.save()
        second_updated_at = main_usr.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        main_usr.save()
        self.assertLess(second_updated_at, main_usr.updated_at)

    def test_save_with_arg(self):
        main_usr = User()
        with self.assertRaises(TypeError):
            main_usr.save(None)

    def test_save_updates_file(self):
        main_usr = User()
        main_usr.save()
        usid = "User." + main_usr.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        main_usr = User()
        self.assertIn("id", main_usr.to_dict())
        self.assertIn("created_at", main_usr.to_dict())
        self.assertIn("updated_at", main_usr.to_dict())
        self.assertIn("__class__", main_usr.to_dict())

    def test_to_dict_contains_added_attributes(self):
        main_usr = User()
        main_usr.middle_name = "Holberton"
        main_usr.my_number = 98
        self.assertEqual("Holberton", main_usr.middle_name)
        self.assertIn("my_number", main_usr.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        main_usr = User()
        us_dict = main_usr.to_dict()
        self.assertEqual(str, type(us_dict["id"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        main_usr = User()
        main_usr.id = "123456"
        main_usr.created_at = main_usr.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(main_usr.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        main_usr = User()
        self.assertNotEqual(main_usr.to_dict(), main_usr.__dict__)

    def test_to_dict_with_arg(self):
        main_usr = User()
        with self.assertRaises(TypeError):
            main_usr.to_dict(None)


if __name__ == "__main__":
    unittest.main()

