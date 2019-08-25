import pytest
from mypackage import divide_numbers

def test_divide_numbers():
    assert divide_numbers(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide_numbers(1, 0)