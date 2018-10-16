from setuptools import setup
import os

base_dir = os.path.dirname(__file__)

setup(
    name='tktitler',
    version='1.1.0',
    description='A library for dealing with TÅGEKAMMER-titles.',
    long_description=open(os.path.join(base_dir,
                                       'readme.rst')).read(),
    url='https://github.com/TK-IT/web',
    author='TK-IT',
    license='Beerware',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    py_modules=["tktitler"],

    extras_require={
        'test': ['testfixtures', 'coveralls'],
        'build': ['sphinx'],
    },
)
