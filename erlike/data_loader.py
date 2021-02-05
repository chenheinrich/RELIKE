import os
import numpy as np

class DataLoader():

    def __init__(self, dataset='pl18_zmax30'):
        self._dataset = dataset
        self._dir = os.path.join('./erlike/data/', self._dataset) #TODO check portability

    def load_file(self, file_name, **kwargs):
        """Returns data from given file_name for the dataset.

        Args:
            file_name: A string for file name.
            kwargs: keyword arguments for numpy.genfromtxt such as skip_header.
        """
        file_path = os.path.join(self._dir, file_name)
        data = np.genfromtxt(file_path, **kwargs) 
        return data
