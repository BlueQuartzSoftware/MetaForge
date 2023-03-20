import os
from setuptools import setup, find_packages

dirname = os.path.dirname(__file__)
readme_filename = os.path.join(dirname, 'README.md')

with open(readme_filename, 'r') as file:
    long_description = file.read()

setup(
  name='metaforge',
  version='1.0.0-rc13',
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
  python_requires='>=3.8',
  include_package_data=True,
  zip_safe=False
)
