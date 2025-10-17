import json
import re

class UserRegister:
    EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$")
    IPV4_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

    def __init__(self, json_files):
        self.users = {}
        for file in json_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Failed to load {file}: {e}")
                continue
            for user in data:
                email = user.get('email')
                ip = user.get('ip')
                name = user.get('name')
                devices = user.get('devices', [])
                if not self._valid_email(email):
                    print(f"Invalid email: {email} in {file}")
                    continue
                if not self._valid_ipv4(ip):
                    print(f"Invalid IPv4: {ip} for {email} in {file}")
                    continue
                if email in self.users:
                    self.users[email]['devices'] = list(set(self.users[email]['devices']) | set(devices))
                else:
                    self.users[email] = {
                        'name': name,
                        'ip': ip,
                        'devices': list(set(devices))
                    }

    def _valid_email(self, email):
        return bool(email and self.EMAIL_REGEX.match(email))

    def _valid_ipv4(self, ip):
        if not ip or not self.IPV4_REGEX.match(ip):
            return False
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)

    def __len__(self):
        return len(self.users)

    def __getitem__(self, email):
        return self.users[email]

    def __setitem__(self, email, value):
        self.users[email] = value

    def __add__(self, other):
        new_register = UserRegister([])
        new_register.users = {**self.users}
        for email, data in other.users.items():
            if email in new_register.users:
                new_register.users[email]['devices'] = list(set(new_register.users[email]['devices']) | set(data['devices']))
            else:
                new_register.users[email] = data.copy()
        return new_register

    def __mul__(self, other):
        new_register = UserRegister([])
        for email in set(self.users) & set(other.users):
            data1 = self.users[email]
            data2 = other.users[email]
            merged_devices = list(set(data1['devices']) | set(data2['devices']))
            new_register.users[email] = {
                'name': data1['name'],
                'ip': data1['ip'],
                'devices': merged_devices
            }
        return new_register