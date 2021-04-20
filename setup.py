from setuptools import setup, find_packages

setup(
    name="relike", 
    version='0.0.1',
    author='Chen Heinrich',
    author_email='chenhe@caltech.edu',
    description=('Python package for the Reionization Effective Likelihood (RELIKE) from Planck 2018 data'),
    url='https://github.com/chenheinrich/RELIKE',
    license='BSD',

    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['scipy>=1.6.0', 'numpy>=1.18.5', 
        'pytest>=5.4.3', 'profiler>=0.1.0'],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={"": ["data/*.dat", "data/*.yaml"]},
    )