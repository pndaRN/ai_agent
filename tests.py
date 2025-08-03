#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path so we can import functions
sys.path.insert(0, '.')

from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test_cli_expected_cases():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    test_cli_expected_cases()

