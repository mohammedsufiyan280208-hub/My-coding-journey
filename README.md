# # Password Generator

This project is a simple Python script that generates a random password based on the length entered by the user.

## Description

The script asks for the password length and then creates a secure random password using letters and digits.

## Requirements

- Python 3 installed on your computer

## How to run

1. Rename the file from `password generator.txt` to `password_generator.py`.
2. Open a terminal in the project folder.
3. Run:

```bash
python password_generator.py
```

4. Enter the password length when prompted.

## Example

```bash
Enter password length: 12
Your password is: a8Kp2mQ7xL1n
```

## Features

- Generates random passwords
- Uses letters and numbers
- Easy to customize

## Code

```python
import random
import string

length = int(input("Enter password length: "))

characters = string.ascii_letters + string.digits

password = ''.join(random.choice(characters) for _ in range(length))

print("Your password is:", password)
```
