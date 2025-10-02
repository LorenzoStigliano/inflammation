"""Tests for statistics functions within the Model layer."""

import numpy as np
import numpy.testing as npt
import pytest

@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0]),
        ([[1, 2], [3, 4], [5, 6]], [3, 4]),
        ([[1, 2, 3], [3, 4, 5], [5, 6, 7]], [3, 4, 5])
    ])
def test_daily_mean(test, expected):
    """Test that mean function works for an array of zeros."""
    from inflammation.models import daily_mean

    test_input = np.array(test)
    test_result = np.array(expected)

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_mean(test_input), test_result)

@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0]),
        ([[1, 2], [3, 4], [5, 6]], [5, 6]),
        ([[1, 2, 3], [3, 4, 5], [5, 6, 7]], [5, 6, 7])
    ])
def test_daily_max(test, expected):
    """Test that mean function works for an array of zeros."""
    from inflammation.models import daily_max

    test_input = np.array(test)
    test_result = np.array(expected)

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_max(test_input), test_result)


@pytest.mark.parametrize(
    "test, expected, type_error",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0], None),
        ([[1, 2], [3, 4], [5, 6]], [1, 2], None),
        ([[1, 2, 3], [3, 4, 5], [5, 6, 7]], [1, 2, 3], None),
        ([['Hello', 'there'], ['General', 'Kenobi']], None, TypeError),
    ])
def test_daily_min(test, expected, type_error):
    """Test that mean function works for an array of zeros."""
    from inflammation.models import daily_min

    test_input = np.array(test)
    test_result = np.array(expected)

    if type_error:
        with pytest.raises(TypeError):
            daily_min(test_input)
    else:
        npt.assert_array_equal(daily_min(test_input), test_result)


@pytest.mark.parametrize(
    "test, expected, expect_raises",
    [
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], None),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]], None),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]], None),
        ([[np.nan, 1, 1], [np.nan, 1, 1], [np.nan, 1, 1]], [[0, 1, 1], [0, 1, 1], [0, 1, 1]], None),
        ([[-1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]], ValueError),
        (
            'hello',
            None,
            ValueError,
        ),
        (
            3,
            None,
            ValueError,
        ),
        (
            [1,2,3],
            None,
            ValueError,
        ),
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]],
            None,
        )
    ])
def test_patient_normalise(test, expected, expect_raises):
    """Test normalisation works for arrays of one and positive integers.
       Assumption that test accuracy of two decimal places is sufficient."""
    from inflammation.models import patient_normalise
    if expect_raises is not None:
        with pytest.raises(expect_raises):
            npt.assert_almost_equal(patient_normalise(np.array(test)), np.array(expected), decimal=2)
    else:
        npt.assert_almost_equal(patient_normalise(np.array(test)), np.array(expected), decimal=2)