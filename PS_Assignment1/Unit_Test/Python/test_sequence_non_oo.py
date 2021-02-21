# This is an example of a test module that does not use an
# object-oriented design.

import numpy as np
import pytest
from sequence import Sequence
 
def test_get_nucleotides():
    sequence_str = "GATTACCA"
    sequence = Sequence(sequence_str)
    # Use Python assert command plus the == operator to assert that
    # string in Sequence object is equal to that given to the
    # Sequence constructor.
    # If the equality is False then the assert fails, an
    # AssertionError is raised and the test fails.
    assert sequence_str == sequence.nucleotides, \
        "Nucleotides returned were not those given"
    
def test_get_weight():
    sequence = Sequence("G")
    # Use Python assert command plus the numpy.isclose function to
    # check that a molecular weight for G returned from
    # sequence.get_weight() is the same as the weight recorded
    # for G in the Sequence.WEIGHTS dictionary.
    # np.isclose compares two values to within a given tolerance or
    # delta (atol) here, 0.01.
    # If np.isclose is False then the assert fails, an
    # AssertionError is raised and the test fails.
    assert np.isclose(Sequence.WEIGHTS['G'],
                      sequence.get_weight(), 
                      atol=0.01), \
                      "Weight returned was unexpected"
    
def test_calculate_weight():
    # Similar to the above but testing calculate_weight.
    sequence = Sequence("G")
    assert np.isclose(Sequence.WEIGHTS['G'],
                      Sequence.calculate_weight(sequence), 
                      atol=0.01), \
                      "Weight returned was unexpected"
    
def test_gatttacca():
    # Similar to the above but testing Sequence constructor using a
    # string of valid letters.
    sequence_str = "GATTACCA"
    sequence = Sequence(sequence_str)
    weight = sequence.get_weight()
    expected_weight = 1909.6
    assert np.isclose(expected_weight, weight, atol=0.1), "Unexpected weight"

def test_empty_sequence():
    # Similar to the above but testing Sequence constructor using an
    # empty string. An empty string is accepted as valid by Sequence
    # which assigns it a weight of 0.0.
    sequence = Sequence("")
    assert np.isclose(0, sequence.get_weight(), atol=0.0), "Unexpected weight"

def test_none_sequence_via_pytest():
    # If the Sequence constructor is given an invalid sequence string
    # of None then it will raise an AssertionError.
    # This test uses the pytest.raises function to check that an
    # AssertionError is raised. If so then the test passes.
    # If an AssertionError was not raised and None was accepted then
    # the test would, as we expect, fail.
    with pytest.raises(AssertionError):
        sequence = Sequence(None)

def test_invalid_sequence_via_pytest():
    # Similar to the above but testing the Sequence constructor with
    # a string of invalid (non-G,A,T,C) characters.
    with pytest.raises(AssertionError):
        sequence = Sequence("XXXXX")
