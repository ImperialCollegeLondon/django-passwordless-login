from pathlib import Path

from setuptools import find_packages, setup

with Path("requirements.txt").open("r") as f:
    dependencies = f.readlines()

with Path("README.md").open("r") as f:
    long_description = f.read()

setup(
    name="django-passwordless-login",
    version="0.0.3",
    description="Login to your Django app with a link sent by email.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ImperialCollegeLondon/django-passwordless-login",
    author="Adrian D'Alessandro",
    author_email="a.dalessandro@imperial.ac.uk",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=dependencies,
    extras_require={},
    packages=find_packages("."),
    include_package_data=True,
)
