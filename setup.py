import os
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "flask_simple_api", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

_INSTALL_REQUIRES = [
    "Flask",
    "Flask-Restful",
    "Logbook",
    "sentinels",
]

setup(name="flask-simple-api",
      classifiers = [
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          ],
      description="Simple API endpoints for Flask using Flask-Restful reqparse and Python 3 annotations",
      license="BSD3",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),

      url="https://github.com/vmalloc/flask-simple-api",

      install_requires=_INSTALL_REQUIRES,
      scripts=[],
      namespace_packages=[]
      )
