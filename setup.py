import os
from setuptools import setup, find_packages
from pathlib import Path

parent_path = Path(__file__).parent

readme_filepath = parent_path / 'README.md'
with open(str(readme_filepath), 'r') as file:
    long_description = file.read()

version_filepath = parent_path / 'metaforge' / 'VERSION'
with open(str(version_filepath)) as version_file:
    version = version_file.read().strip()

setup(
  name='metaforge',
  version=version,
  author='BlueQuartz Software, LLC',
  author_email='info@bluequartz.net',
  description='MetaForge is a Python package for extracting metadata from files using templates, and uploading that metadata to HyperThought',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/BlueQuartzSoftware/MetaForge',
  packages=find_packages(),
  license='BSD',
  platforms='any',
  classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: BSD License'
  ],
  entry_points={
        'gui_scripts': [
            'metaforge = metaforge.__main__:main',
        ]
    },
  package_data={"metaforge": ["VERSION"]},
  python_requires='>=3.8',
  include_package_data=True,
  zip_safe=False
)
