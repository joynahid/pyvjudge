#!/usr/bin/env python

from setuptools import setup, find_packages
from pyvjudge import __version__

setup(
    name="pyvjudge",
    version=__version__,
    python_requires=">=3.7",
    description="Python Vjudge Client",
    author="Nahid H.",
    author_email="info@nahidhq.com",
    url="",
    packages=find_packages(),
    install_requires=["httpx>=0.23.0", "beautifulsoup4>=4.11.1"],
)
