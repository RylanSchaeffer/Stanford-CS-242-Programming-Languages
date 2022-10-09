import numpy as np

# Fudge the path a little bit to keep the directory structure of the homework clean.
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from numpy_problems import find_missing, skyline, matched

# Tests for find_missing.
def test_find_missing():
    assert(np.array_equal(find_missing(4, np.array([0, 1, 2, 3])), np.array([])))
    assert(np.array_equal(find_missing(4, np.array([])), np.array([0, 1, 2, 3])))
    assert(np.array_equal(find_missing(6, np.array([0, 2, 5])), np.array([1, 3, 4])))


# Tests for skyline.
def test_skyline():
    assert(skyline(np.array([5, 5, 5])) == 1)
    assert(skyline(np.array([1, 2, 3, 4, 5])) == 5)
    assert(skyline(np.array([5, 5, 2, 10, 3, 15, 10])) == 3)


# Tests for matched.
def test_matched():
    assert(matched(np.array(['(', ')'])))
    assert(not matched(np.array(['('])))
    assert(not matched(np.array(['(', ')', ')'])))
    assert(not matched(np.array([')', ')', '(', '('])))


test_find_missing()
test_skyline()
test_matched()
print('All tests passed!')
