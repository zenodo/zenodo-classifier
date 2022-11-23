from setuptools import find_packages, setup

setup(
    name='zenodo-classifier',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    version='0.1.0',
    description='Spam classification machine learning models for Zenodo records and communities.',
    author='CERN',
    license='MIT',
)
