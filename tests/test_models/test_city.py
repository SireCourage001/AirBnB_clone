#!/usr/bin/python3
"""Defines unittests for models/city.py.
Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        main_cty = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(main_cty))
        self.assertNotIn("state_id", main_cty.__dict__)

    def test_name_is_public_class_attribute(self):
        main_cty = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(main_cty))
        self.assertNotIn("name", main_cty.__dict__)

    def test_two_cities_unique_ids(self):
        cty_inst_one = City()
        cty_inst_two = City()
        self.assertNotEqual(cty_inst_one.id, cty_inst_two.id)

    def test_two_cities_different_created_at(self):
        cty_inst_one = City()
        sleep(0.05)
        cty_inst_two = City()
        self.assertLess(cty_inst_one.created_at, cty_inst_two.created_at)

    def test_two_cities_different_updated_at(self):
        cty_inst_one = City()
        sleep(0.05)
        cty_inst_two = City()
        self.assertLess(cty_inst_one.updated_at, cty_inst_two.updated_at)

    def test_str_representation(self):
        the_datym = datetime.today()
        dt_repr = repr(the_datym)
        main_cty = City()
        main_cty.id = "123456"
        main_cty.created_at = main_cty.updated_at = the_datym
        cystr = main_cty.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_unused(self):
        main_cty = City(None)
        self.assertNotIn(None, main_cty.__dict__.values())

    def test_instantiation_with_kwargs(self):
        the_datym = datetime.today()
        dt_iso = the_datym.isoformat()
        main_cty = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(main_cty.id, "345")
        self.assertEqual(main_cty.created_at, the_datym)
        self.assertEqual(main_cty.updated_at, the_datym)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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
        main_cty = City()
        sleep(0.05)
        first_updated_at = main_cty.updated_at
        main_cty.save()
        self.assertLess(first_updated_at, main_cty.updated_at)

    def test_two_saves(self):
        main_cty = City()
        sleep(0.05)
        first_updated_at = main_cty.updated_at
        main_cty.save()
        second_updated_at = main_cty.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        main_cty.save()
        self.assertLess(second_updated_at, main_cty.updated_at)

    def test_save_with_arg(self):
        main_cty = City()
        with self.assertRaises(TypeError):
            main_cty.save(None)

    def test_save_updates_file(self):
        main_cty = City()
        main_cty.save()
        ctyid = "City." + main_cty.id
        with open("file.json", "r") as f:
            self.assertIn(ctyid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """ the Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        main_cty = City()
        self.assertIn("id", main_cty.to_dict())
        self.assertIn("created_at", main_cty.to_dict())
        self.assertIn("updated_at", main_cty.to_dict())
        self.assertIn("__class__", main_cty.to_dict())

    def test_to_dict_contains_added_attributes(self):
        main_cty = City()
        main_cty.middle_name = "Holberton"
        main_cty.my_number = 98
        self.assertEqual("Holberton", main_cty.middle_name)
        self.assertIn("my_number", main_cty.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        main_cty = City()
        cy_dict = main_cty.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        the_datym = datetime.today()
        main_cty = City()
        main_cty.id = "123456"
        main_cty.created_at = main_cty.updated_at = the_datym
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': the_datym.isoformat(),
            'updated_at': the_datym.isoformat(),
        }
        self.assertDictEqual(main_cty.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        main_cty = City()
        self.assertNotEqual(main_cty.to_dict(), main_cty.__dict__)

    def test_to_dict_with_arg(self):
        main_cty = City()
        with self.assertRaises(TypeError):
            main_cty.to_dict(None)


if __name__ == "__main__":
    unittest.main()

