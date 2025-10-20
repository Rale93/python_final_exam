import unittest 
from ..src.user_register import UserRegister 

class TestUserRegister(unittest.TestCase):

    def setUp(self):
        """Load existing JSON files before each test"""
        # These files already exist in the project data directory
        self.json_files = [
            "users1.json",
            "users2.json",
            "users3.json",
            "users4.json"
        ]
        self.reg = UserRegister(self.json_files)

    # Test 1: setUp loads JSON files
    def test_setup_loads_json_files(self):
        """Verify that JSON files are successfully loaded"""
        self.assertIsNotNone(self.reg)
        self.assertGreater(len(self.reg.users), 0, "No users were loaded from JSON files")

    # Test 2: __init__ email i IP counter created
    def test_init_creates_counters(self):
        """Check that email and IP counters are initialized"""
        self.assertIsInstance(self.reg.email_counter, dict)
        self.assertIsInstance(self.reg.ip_counter, dict)
        self.assertGreaterEqual(sum(self.reg.email_counter.values()), len(self.reg.users))
        self.assertGreaterEqual(sum(self.reg.ip_counter.values()), len(self.reg.users))