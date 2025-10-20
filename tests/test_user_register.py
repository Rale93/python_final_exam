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

    # Test 6: __getitem__ returns user data
    def test_getitem(self):
        """Test __getitem__ returns correct user data by email"""
        for email in self.reg.user:
            user = self.reg[email]
            self.assertIn(email, self.reg.users)
            self.assertEqual(user, self.reg.users[email])

            self.assertIsInstance(user['name'], str)
            self.assertIsInstance(user['ip'], str)
            self.assertIsInstance(user['devices'], list)

    # Test 7: __setitem__ updates or adds a user
    def test_setitem(self):
        """Test __setitem__ adds a new user or updates existing one"""
        new_email = "urosradic92@gmail.com"
        new_user_data = {
            "name": "Uros Radic",
            "ip": "192.168.170.15",
            "devices": [
                "desktop RTRK-88",
                "lamp F-3285"
            ]
        }
        self.reg[new_email] = new_user_data
        self.assertIn(new_email, self.reg.users)
        self.assertEqual(self.reg[new_email],  new_user_data)

        self.assertEqual(self.reg.get_name(new_email), "Uros Radic")
        self.assertEqual(self.reg.get_ip(new_email), "192.168.170.15")
        self.assertCountEqual(self.reg.get_devices(new_email), ["desktop RTRK-88", "lamp F-3285"])

        updated_user_data = {
            "name": "Marko Radic",
            "ip": "192.168.170.22",
            "devices": [
                "desktop RTRK-99",
            ]
        }
        self.reg[new_email] = updated_user_data
        self.assertIn(new_email, self.reg.users)
        self.assertEqual(self.reg[new_email],  updated_user_data)

        self.assertEqual(self.reg.get_name(new_email), "Marko Radic")
        self.assertEqual(self.reg.get_ip(new_email), "192.168.170.22")
        self.assertCountEqual(self.reg.get_devices(new_email), ["desktop RTRK-99"])

    # Test 8: get_name returns user name
    def test_get_name(self):
        """Test get_name returns user name"""
        for email, user in self.reg.user.items():
            name = self.reg.get_name(email)
            self.assertIsInstance(name, str)
            self.assertEqual(name, user["name"])
            self.assertGreater(len(name), 0, f"Name should not be empty for {email}")

    # Test 9: get_ip returns user ip address
    def test_get_ip(self):
        """Test get_ip returns user ip address"""
        for email, user in self.reg.user.items():
            ip = self.reg.get_ip(email)
            self.assertIsInstance(ip, str)
            self.assertEqual(ip, user["ip"])