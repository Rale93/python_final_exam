import json
import re
import os
from pathlib import Path
from collections import Counter

class UserRegister:
    EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$")
    IPV4_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

    def __init__(self, json_files):
        self.users = {}
        self.email_counter = Counter()
        self.ip_counter = Counter()

        for file in json_files:
            try:
                with open(file, 'r') as f:
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

                self.email_counter[email] += 1
                self.ip_counter[ip] += 1

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
    
    def duplicate_emails(self):
        return {email: count for email, count in self.email_counter.items() if count > 1}

    def duplicate_ips(self):
        return {ip: count for ip, count in self.ip_counter.items() if count > 1}

    def __len__(self):
        return len(self.users)

    def __getitem__(self, email):
        return self.users[email]

    def __setitem__(self, email, value):
        self.users[email] = value
  
    def get_name(self, email):
        return self.users[email]["name"]

    def get_ip(self, email):
        return self.users[email]["ip"]

    def get_devices(self, email):
        return self.users[email]["devices"]

    def set_name(self, email, name):
        self.users[email]["name"] = name

    def set_ip(self, email, ip):
        if self._valid_ipv4(ip):
            self.users[email]["ip"] = ip
        else:
            print(f"Invalid IP format address: {ip}, enter valid format.")

    def set_devices(self, email, devices):
        self.users[email]["devices"] = devices

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

if __name__ == "__main__":

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    files = list(Path(data_dir).glob("*.json"))
    file_paths = [str(f) for f in files]

    print("Found JSON files:")
    for f in file_paths:
        print(f)

    register = UserRegister(file_paths)
    print(f"\nNumber of the valid users: {len(register)}\n")

    print("List of users inside register (name, email, devices, IP address):\n")
    for email, user in register.users.items():
        print(f"Name: {user['name']}, Email: {email}, Devices: {user['devices']}, IP: {user['ip']}")

    print(f"\nNumber of unique duplicate emails and IPs (total): {len(register.duplicate_emails()) + len(register.duplicate_ips())}\n")

    print(f"List of duplicate emails: {register.duplicate_emails()}\n")

    print(f"List of duplicate ip addresses: {register.duplicate_ips()}\n")
