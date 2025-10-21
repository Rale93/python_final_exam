
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.user_register import UserRegister

class TestUserRegister(unittest.TestCase):

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
        for email in self.reg.users:
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
        for email, user in self.reg.users.items():
            name = self.reg.get_name(email)
            self.assertIsInstance(name, str)
            self.assertEqual(name, user["name"])
            self.assertGreater(len(name), 0, f"Name should not be empty for {email}")

    # Test 9: get_ip returns user ip address
    def test_get_ip(self):
        """Test get_ip returns user ip address"""
        for email, user in self.reg.users.items():
            ip = self.reg.get_ip(email)
            self.assertIsInstance(ip, str)
            self.assertEqual(ip, user["ip"])
            
    # Test 10: get_devices returns user devices
    def test_get_devices(self):
        """Test get_devices returns user devices list"""
        for email, user in self.reg.users.items():
            devices = self.reg.get_devices(email)
            self.assertIsInstance(devices, list)
            self.assertEqual(set(devices), set(user["devices"]))

    # Test 11: set_name updates user name
    def test_set_name(self):
        """Test set_name updates the user's name"""
        for email in list(self.reg.users.keys())[:2]:
            self.reg.set_name(email, "Test Name")
            self.assertEqual(self.reg.get_name(email), "Test Name")

    # Test 12: set_ip updates user ip if valid, does not update if invalid
    def test_set_ip(self):
        email = list(self.reg.users.keys())[0]
        valid_ip = "8.8.8.8"
        invalid_ip = "999.999.999.999"
        self.reg.set_ip(email, valid_ip)
        self.assertEqual(self.reg.get_ip(email), valid_ip)
        old_ip = self.reg.get_ip(email)
        self.reg.set_ip(email, invalid_ip)
        self.assertEqual(self.reg.get_ip(email), old_ip)

    # Test 13: set_devices updates user devices
    def test_set_devices(self):
        email = list(self.reg.users.keys())[0]
        new_devices = ["DeviceA", "DeviceB"]
        self.reg.set_devices(email, new_devices)
        self.assertEqual(set(self.reg.get_devices(email)), set(new_devices))

    # Test 14: duplicate_emails returns correct duplicates
    def test_duplicate_emails(self):
        dups = self.reg.duplicate_emails()
        for email, count in dups.items():
            self.assertGreaterEqual(count, 2)

    # Test 15: duplicate_ips returns correct duplicates
    def test_duplicate_ips(self):
        dups = self.reg.duplicate_ips()
        for ip, count in dups.items():
            self.assertGreaterEqual(count, 2)

    # Test 16: __add__ merges registers
    def test_add_operator(self):
        reg2 = UserRegister(self.json_files)
        merged = self.reg + reg2
        self.assertIsInstance(merged, UserRegister)
        for email in self.reg.users:
            self.assertIn(email, merged.users)
            self.assertEqual(set(merged.get_devices(email)), set(self.reg.get_devices(email)))

    # Test 17: __mul__ intersects registers
    def test_mul_operator(self):
        reg2 = UserRegister(self.json_files)
        intersected = self.reg * reg2
        self.assertIsInstance(intersected, UserRegister)
        for email in intersected.users:
            self.assertIn(email, self.reg.users)
            self.assertIn(email, reg2.users)

if __name__ == "__main__":
    unittest.main()
