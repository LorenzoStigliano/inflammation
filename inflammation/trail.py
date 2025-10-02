import numpy as np

from inflammation.patient import Patient

class Trial:
    def __init__(self, data, id):
        self.data = data
        self.id = id

    @classmethod
    def from_csv(cls, filename, id):
        data = cls.load_csv(filename)
        return cls(data, id)

    @staticmethod
    def load_csv(filename):
        return np.loadtxt(fname=filename, delimiter=',')

    def get_patient(self, patient_id):
        row = self.data[patient_id, :] # The first row of the 2D data array
        return Patient(patient_id, row) # Create a Patient with id 0

    def daily_mean(self):
        """Calculate the daily mean of a 2d inflammation data array."""
        return np.mean(self.data, axis=0)


    def daily_max(self):
        """Calculate the daily max of a 2d inflammation data array."""
        return np.max(self.data, axis=0)

    def daily_min(self):
        """Calculate the daily min of a 2d inflammation data array."""
        return np.min(self.data, axis=0)

    def patient_normalise(self):
        if not isinstance(self.data, np.ndarray):
            raise TypeError("Incorrect data type")
        if len(self.data.shape) != 2:
                raise ValueError('inflammation array should be 2-dimensional')
        if np.any(self.data < 0):
            raise ValueError('Inflammation values should not be negative')
        """Normalise patient data from a 2D inflammation data array."""
        max_data = np.nanmax(self.data, axis=1)
        with np.errstate(invalid='ignore', divide='ignore'):
            normalised = self.data / max_data[:, np.newaxis]
        normalised[np.isnan(normalised)] = 0
        normalised[normalised < 0] = 0
        return normalised