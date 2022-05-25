#!/usr/bin/env python

from setuptools import setup, find_packages
from pyvjudge import __version__

setup(
      name='pyvjudge',
      version=__version__,
      python_requires=">=3.7",
      description='Python Vjudge Client',
      author='Nahid Hasan',
      author_email='nahidhasan282@gmail.com',
      url='',
      packages=find_packages(),
      )
