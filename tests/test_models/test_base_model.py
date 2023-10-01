#!/usr/bin/python3
""" """
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models import storage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity
    def test_name2(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

class TestAmenity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up database connection for testing """
  
        cls.engine = create_engine('sqlite:///test_db.sqlite')
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        BaseModel.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        """ Tear down database after testing """
        cls.session.close()
        BaseModel.metadata.drop_all(cls.engine)
        os.remove('test_db.sqlite')
    def setUp(self):

        """ Create a new session for each test """
        self.session = self.Session()
    def tearDown(self):

        """ Clean up the session after each test """
        self.session.rollback()
        self.session.close()
    def test_amenity_table_exists(self):

        """ Test if the 'amenities' table exists in the database """
        self.assertTrue(Amenity.__table__.exists(self.engine))
    def test_amenity_attributes(self):

        """ Test if the Amenity class has the expected attributes """
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'name'))
        self.assertEqual(amenity.name, "")
    def test_amenity_creation(self):

        """ Test creating a new Amenity object """
        amenity_data = {'name': 'Swimming Pool'}
        amenity = Amenity(**amenity_data)
        self.assertEqual(amenity.name, 'Swimming Pool')
    def test_amenity_save_to_database(self):

        """ Test saving an Amenity object to the database """
        amenity_data = {'name': 'Fitness Center'}
        amenity = Amenity(**amenity_data)
        self.session.add(amenity)
        self.session.commit()
        self.assertIn(amenity, self.session.query(Amenity).all())

    def test_amenity_deletion_from_database(self):
        """ Test deleting an Amenity object from the database """
        amenity_data = {'name': 'Sauna'}
        amenity = Amenity(**amenity_data)
        self.session.add(amenity)
        self.session.commit()
        self.session.delete(amenity)
        self.session.commit()
        self.assertNotIn(amenity, self.session.query(Amenity).all())

if __name__ == '__main__':
    unittest.main()
