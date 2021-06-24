#!/usr/bin/env python3
import os

from distutils.core import setup

# Read requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="sample_code_1",
    version="1.2",
    packages=["sample_1"],
    url="https://github.com/FrancoJim/sample_code_1",
    license="MIT",
    author="Kevin Lang",
    author_email="k.j.lang.tech@gmail.com",
    description="USD coin distributer",
    install_requires=requirements,
)
