"""Tests for the Patient model."""
from inflammation.patient import Patient

class TestPatient:

    def setup_class(self):
        self.p = Patient(id=1, data=[1,2,3])

    def test_create_patient(self):
        assert self.p.id == 1

    def test_patient_daily_mean(self):
        assert self.p.daily_mean() == 2

    def test_patient_daily_max(self):
        assert self.p.daily_max() == 3

    def test_patient_daily_min(self):
        assert self.p.daily_min() == 1
