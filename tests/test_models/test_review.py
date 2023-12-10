#!/usr/bin/python3
"""Defines unittests for models/review.py.
Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        main_rvw = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(main_rvw))
        self.assertNotIn("place_id", main_rvw.__dict__)

    def test_user_id_is_public_class_attribute(self):
        main_rvw = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(main_rvw))
        self.assertNotIn("user_id", main_rvw.__dict__)

    def test_text_is_public_class_attribute(self):
        main_rvw = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(main_rvw))
        self.assertNotIn("text", main_rvw.__dict__)

    def test_two_reviews_unique_ids(self):
        rvw_inst_1 = Review()
        rvw_inst_2 = Review()
        self.assertNotEqual(rvw_inst_1.id, rvw_inst_2.id)

    def test_two_reviews_different_created_at(self):
        rvw_inst_1 = Review()
        sleep(0.05)
        rvw_inst_2 = Review()
        self.assertLess(rvw_inst_1.created_at, rvw_inst_2.created_at)

    def test_two_reviews_different_updated_at(self):
        rvw_inst_1 = Review()
        sleep(0.05)
        rvw_inst_2 = Review()
        self.assertLess(rvw_inst_1.updated_at, rvw_inst_2.updated_at)

    def test_str_representation(self):
        the_datym = datetime.today()
        dt_repr = repr(the_datym)
        main_rvw = Review()
        main_rvw.id = "123456"
        main_rvw.created_at = main_rvw.updated_at = the_datym
        rvw_str = main_rvw.__str__()
        self.assertIn("[Review] (123456)", rvw_str)
        self.assertIn("'id': '123456'", rvw_str)
        self.assertIn("'created_at': " + dt_repr, rvw_str)
        self.assertIn("'updated_at': " + dt_repr, rvw_str)

    def test_args_unused(self):
        main_rvw = Review(None)
        self.assertNotIn(None, main_rvw.__dict__.values())

    def test_instantiation_with_kwargs(self):
        the_datym = datetime.today()
        dt_iso = the_datym.isoformat()
        main_rvw = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(main_rvw.id, "345")
        self.assertEqual(main_rvw.created_at, the_datym)
        self.assertEqual(main_rvw.updated_at, the_datym)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        main_rvw = Review()
        sleep(0.05)
        first_updated_at = main_rvw.updated_at
        main_rvw.save()
        self.assertLess(first_updated_at, main_rvw.updated_at)

    def test_two_saves(self):
        main_rvw = Review()
        sleep(0.05)
        first_updated_at = main_rvw.updated_at
        main_rvw.save()
        second_updated_at = main_rvw.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        main_rvw.save()
        self.assertLess(second_updated_at, main_rvw.updated_at)

    def test_save_with_arg(self):
        main_rvw = Review()
        with self.assertRaises(TypeError):
            main_rvw.save(None)

    def test_save_updates_file(self):
        main_rvw = Review()
        main_rvw.save()
        rvid = "Review." + main_rvw.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        main_rvw = Review()
        self.assertIn("id", main_rvw.to_dict())
        self.assertIn("created_at", main_rvw.to_dict())
        self.assertIn("updated_at", main_rvw.to_dict())
        self.assertIn("__class__", main_rvw.to_dict())

    def test_to_dict_contains_added_attributes(self):
        main_rvw = Review()
        main_rvw.middle_name = "Holberton"
        main_rvw.my_number = 98
        self.assertEqual("Holberton", main_rvw.middle_name)
        self.assertIn("my_number", main_rvw.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        main_rvw = Review()
        rv_dict = main_rvw.to_dict()
        self.assertEqual(str, type(rv_dict["id"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["updated_at"]))

    def test_to_dict_output(self):
        the_datym = datetime.today()
        main_rvw = Review()
        main_rvw.id = "123456"
        main_rvw.created_at = main_rvw.updated_at = the_datym
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': the_datym.isoformat(),
            'updated_at': the_datym.isoformat(),
        }
        self.assertDictEqual(main_rvw.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        main_rvw = Review()
        self.assertNotEqual(main_rvw.to_dict(), main_rvw.__dict__)

    def test_to_dict_with_arg(self):
        main_rvw = Review()
        with self.assertRaises(TypeError):
            main_rvw.to_dict(None)


if __name__ == "__main__":
    unittest.main()

