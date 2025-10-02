import pytest
import numpy as np
import numpy.testing as npt

from inflammation.trail import Trial

@pytest.fixture()
def trial_instance():
    return Trial(np.array([[0, 0],[0, 0]]), 1)


class TestTrial:
    def test_daily_mean_zeros(self, trial_instance):
        """Test that mean function works for an array of zeros."""
        trial_instance.data = np.array([
            [0, 0],
            [0, 0],
            [0, 0]])
        test_result = np.array([0, 0])

        # Need to use Numpy testing functions to compare arrays
        npt.assert_array_equal(trial_instance.daily_mean(), test_result)


    def test_daily_mean_integers(self, trial_instance):
        """Test that mean function works for an array of positive integers."""

        trial_instance.data = np.array([
            [1, 2],
            [3, 4],
            [5, 6]])
        test_result = np.array([3, 4])

        # Need to use Numpy testing functions to compare arrays
        npt.assert_array_equal(trial_instance.daily_mean(), test_result)


    @pytest.mark.parametrize(
        "test, expected",
        [
            ([ [0, 0, 0], [0, 0, 0], [0, 0, 0] ], [0, 0, 0]),
            ([ [4, 2, 5], [1, 6, 2], [4, 1, 9] ], [4, 6, 9]),
            ([ [4, -2, 5], [1, -6, 2], [-4, -1, 9] ], [4, -1, 9]),
        ])
    def test_daily_max(self, test, expected, trial_instance):
        """Test max function works for zeroes, positive integers, mix of positive/negative integers."""
        trial_instance.data = np.array(test)
        npt.assert_array_equal(trial_instance.daily_max(), np.array(expected))
