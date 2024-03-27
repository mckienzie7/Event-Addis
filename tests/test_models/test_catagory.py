#!/usr/bin/python3
"""
Contains the TestCatagoryDocs classes
"""

from datetime import datetime
import inspect
import models
from models import catagory
from models.base_model import BaseModel
import pep8
import pycodestyle
import unittest
Catagory = catagory.Catagory


class TestCatagoryDocs(unittest.TestCase):
    """Tests to check the documentation and style of catagory class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.catagory_f = inspect.getmembers(Catagory, inspect.isfunction)

    def test_pep8_conformance_catagory(self):
        """Test that models/catagory.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/catagory.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_amenity(self):
        """Test that tests/test_models/catagory.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_catagory.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenity_module_docstring(self):
        """Test for the catagory.py module docstring"""
        self.assertIsNot(catagory.__doc__, None,
                         "amenity.py needs a docstring")
        self.assertTrue(len(catagory.__doc__) >= 1,
                        "amenity.py needs a docstring")

    def test_amenity_class_docstring(self):
        """Test for the Catagory class docstring"""
        self.assertIsNot(Catagory.__doc__, None,
                         "Catagory class needs a docstring")
        self.assertTrue(len(Catagory.__doc__) >= 1,
                        "Amenity class needs a docstring")

    def test_amenity_func_docstrings(self):
        """Test for the presence of docstrings in Amenity methods"""
        for func in self.catagory_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestCatagory(unittest.TestCase):
    """Test the Catagory class"""
    def test_is_subclass(self):
        """Test that Catagory is a subclass of BaseModel"""
        amenity = Catagory()
        self.assertIsInstance(catagory, BaseModel)
        self.assertTrue(hasattr(catagory, "id"))
        self.assertTrue(hasattr(catagory, "created_at"))
        self.assertTrue(hasattr(catagory, "updated_at"))

    def test_name_attr(self):
        """Test that Catagory has attribute name, and it's as an empty string"""
        catt = Catagory()
        self.assertTrue(hasattr(catt, "name"))
        self.assertTrue(hasattr(catt, "discription"))

        if models.storage_t == 'db':
            self.assertEqual(catt.name, None)
        else:
            self.assertEqual(catt.name, "")

    def test_discription_attr(self):
        """ Test that Catagory has attribute discription and it's an empty String """

        cat = Catagory()
        self.assertEqual(hasattr(cat, "discription"))
        if models.storage_t == 'db':
            self.assertEqual(cat.discription, None)
        else:
            self.assertEqual(cat.discription, "")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        am = Catagory()
        # print(am.__dict__)
        new_d = am.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in am.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        am = Catagory()
        new_d = am.to_dict()
        self.assertEqual(new_d["__class__"], "Catagory")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], am.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], am.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        catt = Catagory()
        string = "[Catagory] ({}) {}".format(catt.id, catt.__dict__)
        self.assertEqual(string, str(catt))
