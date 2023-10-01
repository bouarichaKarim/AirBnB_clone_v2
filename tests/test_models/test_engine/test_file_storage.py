#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.storage = FileStorage()
        self.storage.reload()

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all(self):
        # Test if all() returns a dictionary
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_cls(self):
        # Test if all(cls) returns a dictionary containing only objects of that class
        user = User()
        user.save()
        place = Place()
        place.save()

        result = self.storage.all(User)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 1)
        self.assertIn(user.id, result)
        self.assertNotIn(place.id, result)

    def test_new(self):
        # Test if new() adds a new object to the storage dictionary
        obj = BaseModel()
        self.storage.new(obj)
        self.assertIn(obj.id, self.storage.all())

    def test_save_and_reload(self):
        # Test if save() and reload() correctly save and reload data
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        new_storage = FileStorage()
        new_storage.reload()
        self.assertEqual(len(self.storage.all()), len(new_storage.all()))
        self.assertIn(obj.id, new_storage.all())

    def test_delete(self):
        # Test if delete() deletes an object from the storage dictionary
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.delete(obj)
        self.assertNotIn(obj.id, self.storage.all())

    def test_reload_nonexistent_file(self):
        # Test if reload() handles the case where the file doesn't exist
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        new_storage = FileStorage()
        new_storage.reload()
        self.assertEqual(len(new_storage.all()), 0)

    def test_reload_empty_file(self):
        # Test if reload() handles the case where the file is empty
        with open("file.json", "w") as f:
            f.write("")
        new_storage = FileStorage()
        new_storage.reload()
        self.assertEqual(len(new_storage.all()), 0)

    def test_reload_invalid_json(self):
        # Test if reload() handles the case where the file contains invalid JSON
        with open("file.json", "w") as f:
            f.write("invalid json")
        new_storage = FileStorage()
        new_storage.reload()
        self.assertEqual(len(new_storage.all()), 0)

if __name__ == '__main__':
    unittest.main()
