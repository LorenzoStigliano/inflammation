import numpy as np

from inflammation.patient import Patient
from inflammation.db import query_database, connect_to_database

class Trial:
    def __init__(self, data, id):
        self.data = data
        self.id = id

    @classmethod
    def from_csv(cls, filename, id):
        """
        Class method to create a Trial instance from data in a CSV file.

        Parameters:
        filename (str): The file path of the CSV file to read.
        id (str): The id to assign to the Trial instance.

        Returns:
        Trial: A Trial instance with the data and id from the CSV file.
        """
        data = cls.load_csv(filename)
        return cls(data, id)

    @classmethod
    def from_database(cls, db_filepath, trial_id):
        """
        Class method to create a Trial instance from data in a SQLite database.

        Parameters:
        db_filepath (str): The file path of the SQLite database to connect to.
        trial_id (str): The trial_id to query the database for.

        Returns:
        Trial: A Trial instance with the data and id from the database.
        """
        query = f'SELECT * FROM data WHERE trial_id = "{trial_id}"'
        connection = connect_to_database(db_filepath)
        data = query_database(query, connection)
        if not data:
            raise ValueError("No data found for trial_id")
        # Convert the list of tuples to a numpy array and skip the first two columns
        if np.shape(data)[0] == 1:  # If only one row is returned, convert to 2D array
            data = np.array([data[0][3:]]).astype(float)
        else:
            data = np.array(data)[:, 3:].astype(float)
        return cls(data, trial_id)

    @staticmethod
    def load_csv(filename):
        """Load a Numpy array from a CSV

        :param filename: Filename of CSV to load
        """
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