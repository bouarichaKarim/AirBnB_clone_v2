import unittest
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv


class TestDBStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the class."""
        cls.storage = DBStorage()
        cls.storage.reload()

    def test_new_instance(self):
        """Test creating a new instance of DBStorage."""
        self.assertIsInstance(self.storage, DBStorage)

    def test_all(self):
        """Test the 'all' method."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        all_objs = self.storage.all()
        self.assertIn(obj, all_objs.values())

    def test_all_with_class(self):
        """Test the 'all' method with a specific class."""
        obj1 = State()
        obj2 = City()
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.save()
        states = self.storage.all(State)
        cities = self.storage.all(City)
        self.assertIn(obj1, states.values())
        self.assertIn(obj2, cities.values())

    def test_new(self):
        """Test the 'new' method."""
        obj = User()
        self.storage.new(obj)
        self.assertIn(obj, self.storage._DBStorage__session.new)

    def test_save(self):
        """Test the 'save' method."""
        obj = Place()
        self.storage.new(obj)
        self.storage.save()
        self.assertIn(obj, self.storage._DBStorage__session)

    def test_delete(self):
        """Test the 'delete' method."""
        obj = Amenity()
        self.storage.new(obj)
        self.storage.save()
        self.storage.delete(obj)
        self.assertNotIn(obj, self.storage._DBStorage__session)

    def test_reload(self):
        """Test the 'reload' method."""
        old_session = self.storage._DBStorage__session
        old_engine = self.storage._DBStorage__engine
        self.storage.reload()
        new_session = self.storage._DBStorage__session
        new_engine = self.storage._DBStorage__engine
        self.assertNotEqual(old_session, new_session)
        self.assertNotEqual(old_engine, new_engine)

    def test_close(self):
        """Test the 'close' method."""
        self.storage.close()
        self.assertIsNone(self.storage._DBStorage__session)


if __name__ == "__main__":
    unittest.main()

