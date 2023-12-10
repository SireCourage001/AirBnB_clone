#!/usr/bin/python3
"""Defines unittests for models/state.py.
Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        main_ste = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(main_ste))
        self.assertNotIn("name", main_ste.__dict__)

    def test_two_states_unique_ids(self):
        st_inst_one = State()
        st_inst_two = State()
        self.assertNotEqual(st_inst_one.id, st_inst_two.id)

    def test_two_states_different_created_at(self):
        st_inst_one = State()
        sleep(0.05)
        st_inst_two = State()
        self.assertLess(st_inst_one.created_at, st_inst_two.created_at)

    def test_two_states_different_updated_at(self):
        st_inst_one = State()
        sleep(0.05)
        st_inst_two = State()
        self.assertLess(st_inst_one.updated_at, st_inst_two.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        main_ste = State()
        main_ste.id = "123456"
        main_ste.created_at = main_ste.updated_at = dt
        ststr = main_ste.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    def test_args_unused(self):
        main_ste = State(None)
        self.assertNotIn(None, main_ste.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        main_ste = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(main_ste.id, "345")
        self.assertEqual(main_ste.created_at, dt)
        self.assertEqual(main_ste.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        main_ste = State()
        sleep(0.05)
        first_updated_at = main_ste.updated_at
        main_ste.save()
        self.assertLess(first_updated_at, main_ste.updated_at)

    def test_two_saves(self):
        main_ste = State()
        sleep(0.05)
        first_updated_at = main_ste.updated_at
        main_ste.save()
        second_updated_at = main_ste.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        main_ste.save()
        self.assertLess(second_updated_at, main_ste.updated_at)

    def test_save_with_arg(self):
        main_ste = State()
        with self.assertRaises(TypeError):
            main_ste.save(None)

    def test_save_updates_file(self):
        main_ste = State()
        main_ste.save()
        stid = "State." + main_ste.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        main_ste = State()
        self.assertIn("id", main_ste.to_dict())
        self.assertIn("created_at", main_ste.to_dict())
        self.assertIn("updated_at", main_ste.to_dict())
        self.assertIn("__class__", main_ste.to_dict())

    def test_to_dict_contains_added_attributes(self):
        main_ste = State()
        main_ste.middle_name = "Holberton"
        main_ste.my_number = 98
        self.assertEqual("Holberton", main_ste.middle_name)
        self.assertIn("my_number", main_ste.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        main_ste = State()
        st_dict = main_ste.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        main_ste = State()
        main_ste.id = "123456"
        main_ste.created_at = main_ste.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(main_ste.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        main_ste = State()
        self.assertNotEqual(main_ste.to_dict(), main_ste.__dict__)

    def test_to_dict_with_arg(self):
        main_ste = State()
        with self.assertRaises(TypeError):
            main_ste.to_dict(None)


if __name__ == "__main__":
    unittest.main()

