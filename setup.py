from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'DESCRIPTION.rst')) as f:
    long_description = f.read()

setup(
    name="relike", 
    version='0.0.1',
    author='Chen Heinrich',
    author_email='chenhe@caltech.edu',
    description='Python package for the Reionization Effective Likelihood (RELIKE) from Planck data',
    long_description_content_type="text/x-rst",
    long_description=long_description,
    url='https://github.com/chenheinrich/RELIKE',
    license='BSD',

    packages=find_packages(include=['relike', 'relike.*']),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['scipy>=1.6.0', 
        'numpy>=1.18.5', 
        'matplotlib>=3.4.1',
        'pyyaml>=5.3.1'],
    python_requires='>=3.8',
    package_data={"relike": ["data/pl18_zmax30/*"]},
    #entry_points={
    #    'console_scripts': ['tanh=relike.example_likelihood:main']
    #},
    )