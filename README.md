# 🧾 Final Project – Python User Register

## 📘 Task Description

Using the **Python programming language**, implement the **user register** according to the specification below.

---

## 🗂️ Input Data

The input data for the program is provided in **JSON files** containing user information.

Each JSON file should include the following fields:

- **Name and surname** – `string`
- **E-mail address** – `string`
- **IPv4 address** (in decimal notation) – `string`
- **List of mapped devices** – `list[string]`

### Requirements:
- Create **at least 4 JSON files**, each containing **at least 8 users**.
- At least **one file must contain a user that already exists** in another file (a duplicate).

---

## ⚙️ Program Requirements

- The program must **load the JSON input files**.
- It should **combine the data** from all JSON files into a **single user register**, printed as program output.
- Users and data may exist in multiple files, so it is important to:
  - **Detect and remove duplicates.**
  - **Merge device lists** if the same user appears in multiple files (perform **set union** of devices).

The **key in the register** is the user’s **e-mail address**.

---

## 🧩 Class Specification

Create a **class representing the user register** with at least the following functionality:

### 🔸 Constructor
- Accepts a **list of input JSON files** as parameters.
- Parses all data and builds the register.
- Validates user data:
  - Checks that **e-mail addresses** and **IPv4 addresses** are in the **correct format**.
  - Discards invalid entries and prints a message about them.

### 🔸 Overloaded Methods
- `len()` → returns the **number of users** in the register.
- Indexing `[]` → access user data **by e-mail key** (both for reading and writing).

### 🔸 Getter Methods
- Provide getter methods for each user attribute **except the e-mail address**  
  (e.g. `get_ip(email)` to return the IPv4 address).

### 🔸 Setter Methods
- Provide setter methods for each user attribute **except the e-mail address**.  
- When changing the **IP address**, validate its format again.

### 🔸 Operator Overloading
- **Addition (`+`)** → merge (union) of two registers  
  → produces a new register containing all unique users.
- **Multiplication (`*`)** → intersection of two registers  
  → produces a new register containing only users present in both.

---

## 🧪 Unit Testing

All parts of the implementation **must be covered by unit tests** to verify:
- Data parsing and validation
- Duplicate removal and device merging
- Getter/setter correctness
- Operator overloading functionality

---

## ✅ Summary

**Goal:** Develop a modular, well-tested Python program that handles user data across multiple JSON files, ensuring data integrity and correctness.

---

📅 *NIT-CE-08 Python Programming – Final Exam Project*
