### Course: NIT-CE-08 Python Programming
### Module: Final Project
### Starter file for the exercise

import json
from pathlib import Path
import os

all_users = []

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
files = list(Path(data_dir).glob("*.json"))

# stampanje svih dostupnih json fajlova
print(files)

# parsiranje json fajlove i pretvaranje u Python listu
for file in files:
    with open(file, "r") as f:
        users = json.load(f)
        all_users.extend(users)
        
print(f"\nUkupno korisnika (uključujući duplikate): {len(all_users)} \n")

print("Korisnici u registru: \n")
for user in all_users:
    print(user['name'])