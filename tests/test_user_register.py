import unittest 
from ..src.user_register import UserRegister 

class TestUserRegister(unittest.TestCase):
    def setUp(self):
        # Test data without files – users simulation
        self.reg1 = UserRegister([])
        self.reg1.users = {
            "pera@gmail.com": {
                "name": "Pera",
                "ip": "192.168.1.10",
                "devices": ["TV", "Phone"]
            },
            "mika@yahoo.com": {
                "name": "Mika",
                "ip": "192.168.1.11",
                "devices": ["Tablet"]
            }
        }

        self.reg2 = UserRegister([])
        self.reg2.users = {
            "pera@gmail.com": {
                "name": "Pera",
                "ip": "192.168.1.10",
                "devices": ["Laptop"]
            },
            "zika@gmail.com": {
                "name": "Zika",
                "ip": "192.168.1.12",
                "devices": ["PC"]
            }
        }

