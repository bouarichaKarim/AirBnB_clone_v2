import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand

class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        self.console = None

    def test_create(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertTrue(output.startswith("Enter the following attributes:"), f"Expected attribute input, got: {output}")

    def test_create_with_attributes(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create BaseModel name='test' age=25")
            output = mock_stdout.getvalue().strip()
            self.assertTrue(output.startswith("Enter the following attributes:"), f"Expected attribute input, got: {output}")

    def test_show(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create BaseModel")
            self.console.onecmd("show BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertTrue("BaseModel" in output, f"Expected 'BaseModel' in output, got: {output}")

    def test_destroy(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create BaseModel")
            self.console.onecmd("destroy BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertTrue("BaseModel" not in output, f"Expected 'BaseModel' to be destroyed, got: {output}")

    def test_all(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.console.onecmd("all")
            output = mock_stdout.getvalue().strip()
            self.assertTrue("BaseModel" in output, f"Expected 'BaseModel' in output, got: {output}")

    def test_count(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create BaseModel")
            self.console.onecmd("count BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "1", f"Expected '1', got: {output}")

if __name__ == '__main__':
    unittest.main()
