import pytest
from project import validate_grid

# GUI code requires refactoring to be "pytested"
def test_valid_grid(): # Valid
    grid = [
        "10011",
        "11010",
        "00000",
        "01101",
        "10111"
    ]
    assert validate_grid(grid) == "Valid"

def test_invalid_row(): # Invalid row
    grid = [
        "11111",  
        "11010",
        "00000",
        "01101",
        "10111"
    ]
    assert validate_grid(grid) == "Invalid"

def test_invalid_column(): # Alters column 2
    grid = [
        "10011",
        "10010",
        "00000",
        "01101",
        "10111"  
    ]
    assert validate_grid(grid) == "Invalid"

def test_non_binary_input(): # Invalid char
    grid = [
        "10011",
        "1101A",  
        "00000",
        "01101",
        "10111"
    ]
    assert validate_grid(grid) == "Invalid"

def test_incorrect_dimensions():
    grid = [
        "10011",
        "11010"
    ]  # Missing rows
    assert validate_grid(grid) == "Invalid"
