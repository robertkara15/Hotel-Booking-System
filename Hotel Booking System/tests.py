# importing the necessary modules and files to test out
import unittest
import db
import login
from random import randint


class TestDatabaseMethods(unittest.TestCase):
    def setUp(self):
        self.mock_db = db.Database()
        self.existing_random_username = "robert" + str(randint(100, 200))
        self.new_random_username = "robert" + str(randint(201, 300))
        print("Existing Username for testing 1: {0}".format(self.existing_random_username))
        print("New Username for testing 2: {0}".format(self.new_random_username))
        self.mock_db.add_user(self.existing_random_username, "testing1234", 0, "employee", "robert", "kara")

    def tearDown(self):
        print("Removing testing username: {0}".format(self.existing_random_username))
        print("Removing testing username: {0}".format(self.new_random_username))
        try:
            self.mock_db.remove_user(self.existing_random_username)
            self.mock_db.remove_user(self.new_random_username)
        except ValueError:
            print("Complete")

    def test_creation_if_no_file(self):
        self.assertTrue(self.mock_db.existing_database_on_disk)

    def test_insert_new_user_record(self):
        role = "employee"
        self.assertEqual("SUCCESS: Username added to database as role: {0}".format(role),
                         self.mock_db.add_user(self.new_random_username, "testing1234", 0, role, "robert", "kara"))

    def test_reinsert_user_record(self):
        with self.assertRaises(ValueError):
            self.mock_db.add_user(self.existing_random_username, "testing5678", 0, "employee", "robert", "kara")

    def test_is_existing_user_check(self):
        self.assertTrue(self.mock_db.is_existing_user(self.existing_random_username))

    def test_is_not_existing_user_check(self):
        self.assertFalse(self.mock_db.is_existing_user(self.new_random_username))


class TestCredentialValidationMethods(unittest.TestCase):

    def test_empty_username(self):
        with self.assertRaises(ValueError):
            login.LoginForm.validate_username(None, "")

    def test_empty_password(self):
        with self.assertRaises(ValueError):
            login.LoginForm.validate_password(None, "")

    def test_none_username(self):
        with self.assertRaises(ValueError):
            login.LoginForm.validate_username(None, None)

    def test_none_password(self):
        with self.assertRaises(ValueError):
            login.LoginForm.validate_password(None, None)

    def test_short_password(self):
        with self.assertRaises(ValueError):
            login.LoginForm.validate_password(None, "test1")

    def test_short_username(self):
        with self.assertRaises(ValueError):
            login.LoginForm.validate_username(None, "lo")

    def test_invalid_username_symbols(self):
        with self.assertRaises(ValueError):
            login.LoginForm.validate_username(None, "kara%1")

    def test_invalid_password_simple(self):
        with self.assertRaises(ValueError):
            login.LoginForm.validate_password(None, "password")

    def test_valid_password(self):
        self.assertTrue(login.LoginForm.validate_password(None, "testing123"))

    def test_valid_username(self):
        self.assertTrue(login.LoginForm.validate_username(None, "robertkara"))


if __name__ == '__main__':
    unittest.main










