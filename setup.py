import os

import setuptools
from setuptools import setup

tests_requires = [
    "pytest",
    "requests",
]

install_requires = [
    "numpy",
    "jieba",
]


setup(
    name=os.getenv("_PKG_NAME", "data_tool"),  # _PKG_NAME will be used in Makefile for dev release
    version="0.0.4",
    packages=setuptools.find_packages(),
    include_package_data=True,
    url="https://github.com/shfshf/data_tool",
    license="Apache 2.0",
    author="Hanfeng Song",
    author_email="1316478299@qq.com",
    description="data_tool",
    install_requires=install_requires,
)
