import io
import os
import re

from setuptools import setup, find_packages


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type("")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="GithubCacher",
    version="0.0.1",  # still in starting phase of dev,
    url="https://github.com/defi-os/github-cacher",
    description="A tool that caches github issues in weaviate to allow for better search experience",
    author="Tanmay Mujal",
    author_email="tanmaymunjal64@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=required,
)
