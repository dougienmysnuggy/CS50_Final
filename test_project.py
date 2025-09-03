import pytest 
from project import format_date, get_mode, get_output_filename, verify_dates, verify_filename

def test_formate_date():
    assert format_date('Aug 25, 1977') == '1977-08-25'
    assert format_date('Dec 25, 2025') == '2025-12-25'
    assert format_date('Jan 1, 1893') == '1893-01-01'
    
def test_get_output_filename():
    assert get_output_filename('2025-01-01', '2025-08-31', True) == 'ebay_income_statment_2025-01-01_2025-08-31'
    assert get_output_filename('2025-07-01', '2025-07-31', False) == 'ebay_income_statment_2025-07-01_2025-07-31.txt'

def test_verify_dates():
    assert verify_dates('2005-01-01') == True
    assert verify_dates('') == False
    assert verify_dates('Aug 25, 1977') == False
    assert verify_dates('2001-01-01') == True
    assert verify_dates('2025-01-32') == False
    
def test_verify_filename():
    assert verify_filename('file.csv') == True
    assert verify_filename('file') == False
    assert verify_filename('file.txt') == False