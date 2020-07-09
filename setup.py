#!/usr/bin/python
# coding: utf-8
"""Setup file for the generation of the RAnalysis python library."""

from setuptools import find_packages, setup

setup(
    name="RAnalysis",
    version="0.1",
    description="Display and plot data from CSV files",
    long_description=open('README.md').read(),
    author='Emmanuel Hermellin',
    author_email='emmanuel.hermellin@onera.fr',
    packages=find_packages(exclude=['tests']),
    zip_safe=False, install_requires=['numpy', 'matplotlib', 're', 'logging', 'csv', 'queue', 'tkinter']
)
