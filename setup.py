from pathlib import Path

from setuptools import find_packages, setup

with Path("requirements.txt").open("r") as f:
    dependencies = f.readlines()

setup(
    name="django-passwordless-login",
    version="0.0.1",
    url="https://github.com/ImperialCollegeLondon/django-passwordless-login",
    author="Research Computing Service, Imperial College London",
    author_email="rcs-support@imperial.ac.uk",
    install_requires=dependencies,
    extras_require={},
    packages=find_packages("."),
    include_package_data=True,
)
