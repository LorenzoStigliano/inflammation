import numpy as np 

class Patient:
    def __init__(self, id, data):
        self.id = id
        self.data = data
    
    def daily_mean(self):
        """Calculate the daily mean of a 2d inflammation data array."""
        return np.mean(self.data)

    def daily_max(self):
        """Calculate the daily max of a 2d inflammation data array."""
        return np.max(self.data)

    def daily_min(self):
        """Calculate the daily min of a 2d inflammation data array."""
        return np.min(self.data)
