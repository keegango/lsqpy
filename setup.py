from setuptools import setup

setup(
    name='lsqpy',
    version='0.01',
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
