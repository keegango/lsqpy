from setuptools import setup
import sys

if sys.version_info < (3, 3):
    sys.exit("lsqpy requires python 3.3 and above")

setup(
    name='lsqpy',
    version='0.02',
    author='Keegan Go',
    author_email='keegango@stanford.edu',
    packages=['lsqpy',
              'lsqpy.exprs',
			  'lsqpy.constraint',
			  'lsqpy.util'],
    package_dir={'lsqpy': 'lsqpy'},
        url='http://github.com/keegango/lsqpy',
    license='...',
    description='A library that provides support for solving least squares optimization problems.',
)
