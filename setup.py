from setuptools import setup

setup(
  name="pdf-comparer",
  version="0.1",
  description="A pdf comparison tool based on ghostscript.",
  url="https://github.com/arachnys/pdf-comparer",
  author="Cedric Cordenier",
  author_email="cedric@arachnys.com",
  packages=['comparer'],
  install_requires=[
    "appdirs==1.4.3",
    "click==6.7",
    "olefile==0.44",
    "packaging==16.8",
    "Pillow==4.1.1",
    "pyparsing==2.2.0",
    "six==1.10.0"
  ],
  test_suite='nose.collector',
  tests_require=['nose']
)
