import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.rst")) as f:
    CHANGES = f.read()

requires = [
        "django==2.1.3",
        "djangorestframework>=3.9.1",
        "markdown==2.6.9",
        "pdfminer==20140328",
        "requests>=2.20.0",
    ]

setup(name="Assignment",
      version="0.1",
      description="PDF Crawler.",
      long_description=README + "\n\n" + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author="Roman Danilov",
      author_email="danil_rom@yahoo.com",
      url="",
      keywords="pdf python django requests",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=["mock"],
  )
