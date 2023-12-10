#!/usr/bin/python3
"""Defines unittests for models/place.py.
Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(main_plc))
        self.assertNotIn("city_id", main_plc.__dict__)

    def test_user_id_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(main_plc))
        self.assertNotIn("user_id", main_plc.__dict__)

    def test_name_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(main_plc))
        self.assertNotIn("name", main_plc.__dict__)

    def test_description_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(main_plc))
        self.assertNotIn("desctiption", main_plc.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(main_plc))
        self.assertNotIn("number_rooms", main_plc.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(main_plc))
        self.assertNotIn("number_bathrooms", main_plc.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(main_plc))
        self.assertNotIn("max_guest", main_plc.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(main_plc))
        self.assertNotIn("price_by_night", main_plc.__dict__)

    def test_latitude_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(main_plc))
        self.assertNotIn("latitude", main_plc.__dict__)

    def test_longitude_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(main_plc))
        self.assertNotIn("longitude", main_plc.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        main_plc = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(main_plc))
        self.assertNotIn("amenity_ids", main_plc.__dict__)

    def test_two_places_unique_ids(self):
        plc_inst_1 = Place()
        plc_inst_2 = Place()
        self.assertNotEqual(plc_inst_1.id, plc_inst_2.id)

    def test_two_places_different_created_at(self):
        plc_inst_1 = Place()
        sleep(0.05)
        plc_inst_2 = Place()
        self.assertLess(plc_inst_1.created_at, plc_inst_2.created_at)

    def test_two_places_different_updated_at(self):
        plc_inst_1 = Place()
        sleep(0.05)
        plc_inst_2 = Place()
        self.assertLess(plc_inst_1.updated_at, plc_inst_2.updated_at)

    def test_str_representation(self):
        the_datym = datetime.today()
        dt_repr = repr(the_datym)
        main_plc = Place()
        main_plc.id = "123456"
        main_plc.created_at = main_plc.updated_at = the_datym
        plc_str = main_plc.__str__()
        self.assertIn("[Place] (123456)", plc_str)
        self.assertIn("'id': '123456'", plc_str)
        self.assertIn("'created_at': " + dt_repr, plc_str)
        self.assertIn("'updated_at': " + dt_repr, plc_str)

    def test_args_unused(self):
        main_plc = Place(None)
        self.assertNotIn(None, main_plc.__dict__.values())

    def test_instantiation_with_kwargs(self):
        the_datym = datetime.today()
        dt_iso = the_datym.isoformat()
        main_plc = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(main_plc.id, "345")
        self.assertEqual(main_plc.created_at, the_datym)
        self.assertEqual(main_plc.updated_at, the_datym)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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
        main_plc = Place()
        sleep(0.05)
        first_updated_at = main_plc.updated_at
        main_plc.save()
        self.assertLess(first_updated_at, main_plc.updated_at)

    def test_two_saves(self):
        main_plc = Place()
        sleep(0.05)
        first_updated_at = main_plc.updated_at
        main_plc.save()
        second_updated_at = main_plc.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        main_plc.save()
        self.assertLess(second_updated_at, main_plc.updated_at)

    def test_save_with_arg(self):
        main_plc = Place()
        with self.assertRaises(TypeError):
            main_plc.save(None)

    def test_save_updates_file(self):
        main_plc = Place()
        main_plc.save()
        plid = "Place." + main_plc.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        main_plc = Place()
        self.assertIn("id", main_plc.to_dict())
        self.assertIn("created_at", main_plc.to_dict())
        self.assertIn("updated_at", main_plc.to_dict())
        self.assertIn("__class__", main_plc.to_dict())

    def test_to_dict_contains_added_attributes(self):
        main_plc = Place()
        main_plc.middle_name = "Holberton"
        main_plc.my_number = 98
        self.assertEqual("Holberton", main_plc.middle_name)
        self.assertIn("my_number", main_plc.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        main_plc = Place()
        pl_dict = main_plc.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        the_datym = datetime.today()
        main_plc = Place()
        main_plc.id = "123456"
        main_plc.created_at = main_plc.updated_at = the_datym
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': the_datym.isoformat(),
            'updated_at': the_datym.isoformat(),
        }
        self.assertDictEqual(main_plc.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        main_plc = Place()
        self.assertNotEqual(main_plc.to_dict(), main_plc.__dict__)

    def test_to_dict_with_arg(self):
        main_plc = Place()
        with self.assertRaises(TypeError):
            main_plc.to_dict(None)


if __name__ == "__main__":
    unittest.main()

