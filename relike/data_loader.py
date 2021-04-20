import os
import numpy as np
import yaml
import pkg_resources

class DataLoader():

    def __init__(self, dataset='pl18_zmax30'):
        self._dataset = dataset
        self._relike_dir = os.path.dirname(os.path.realpath(__file__))
        self._dir = os.path.join('%s/data/'%self._relike_dir, self._dataset) 

    def load_file(self, file_name, **kwargs):
        """Returns data from given file_name for the dataset.

        Args:
            file_name: A string for file name.
            kwargs: keyword arguments for numpy.genfromtxt such as skip_header.
        """
        file_path = os.path.join(self._dir, file_name)
        data = np.genfromtxt(file_path, **kwargs) 
        return data

    def load_yaml(self, file_name, **kwargs):
        """Returns dictionary loaded from a yaml file of given file_name.

        Args:
            file_name: A string for yaml file name.
        """
        file_path = os.path.join(self._dir, file_name)
        with open(file_path) as f:
            dictionary = yaml.safe_load(f)
        return dictionary
