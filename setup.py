from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='TomatoLeafDiseas',
      version="0.0.1",
      description="Disease classification of tomato leaves using Deep Learning",
      license="MIT",
      author="Jaris Fenner",
      author_email="jaris.a.fenner@gmail.com",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      include_package_data=True,
      zip_safe=False)
