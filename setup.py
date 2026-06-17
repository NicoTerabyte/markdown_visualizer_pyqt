from setuptools import setup
from Cython.Build import cythonize

setup(
	name="utils file",
	ext_modules=cythonize("utils.py"),
)
