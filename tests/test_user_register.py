import unittest 
from src.user_register import UserRegister 

class TestUserRegister(unittest.TestCase):
    """Basic unit tests for the UserRegister class."""

    def setUp(self):
        """Initialize the UserRegister using existing JSON files."""
        self.json_files = [
            "data/users1.json",
            "data/users2.json",
            "data/users3.json",
            "data/users4.json"
        ]
        self.reg = UserRegister(self.json_files)

    # Test 1 – verify that __init__ loads user data
    def test_init_loads_json_files(self):
        """Check that JSON files are loaded and contain user records."""
        self.assertIsNotNone(self.reg)
        self.assertGreater(len(self.reg.users), 0, "No users loaded from JSON files")

    # Test 2 – verify that counters are created
    def test_init_creates_counters(self):
        """Ensure that email_counter and ip_counter are initialized."""
        self.assertTrue(hasattr(self.reg, "email_counter"))
        self.assertTrue(hasattr(self.reg, "ip_counter"))
        self.assertIsInstance(self.reg.email_counter, dict)
        self.assertIsInstance(self.reg.ip_counter, dict)

    # Test 3 – validate email formats
    def test_valid_email(self):
        """Validate correct and incorrect email formats."""
        valid = ["pera@gmail.com", "mika.petrovic@company.co", "user123@mail.rs"]
        invalid = ["invalid@", "user@domain", "plainaddress", "@missing"]

        for e in valid:
            self.assertTrue(self.reg._valid_email(e), f"Expected valid email: {e}")
        for e in invalid:
            self.assertFalse(self.reg._valid_email(e), f"Expected invalid email: {e}")

    # Test 4 – validate IPv4 addresses
    def test_valid_ipv4(self):
        """Validate correct and incorrect IPv4 address formats."""
        valid = ["192.168.0.1", "10.0.0.5", "255.255.255.255", "0.0.0.0"]
        invalid = ["256.0.0.1", "192.168.1", "abc.def.ghi.jkl", "192.168.1.999"]

        for ip in valid:
            self.assertTrue(self.reg._valid_ipv4(ip), f"Expected valid IPv4: {ip}")
        for ip in invalid:
            self.assertFalse(self.reg._valid_ipv4(ip), f"Expected invalid IPv4: {ip}")

    # Test 5 – verify __len__ method
    def test_len_method(self):
        """Check that __len__ returns the number of users correctly."""
        before = len(self.reg)
        self.assertGreater(before, 0, "Register should not be empty")

        # Add a new user and ensure the count increases
        self.reg.users["new_user@mail.com"] = {
            "name": "New",
            "ip": "10.0.0.7",
            "devices": ["SmartTV"]
        }
        after = len(self.reg)
        self.assertEqual(after, before + 1, "Length did not increase after adding user")

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