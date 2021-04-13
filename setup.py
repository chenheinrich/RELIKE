from setuptools import setup, find_packages

setup(name="relike", 
    packages=find_packages(),
    install_requires=['scipy>=1.6.0', 'numpy>=1.18.5', 
        'pytest>=5.4.3', 'profiler>=0.1.0'],
    python_requires='>=3.6')