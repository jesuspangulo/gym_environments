import setuptools
from setuptools import setup

setup(
    name="gym_environments",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=["gym==0.26.2", "numpy==1.23.5", "pygame", "box2d-py"],
)
