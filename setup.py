#!/usr/bin/env python
#coding: utf-8
from setuptools import setup

import sys
import os
reload(sys).setdefaultencoding("UTF-8")

def get_long_desc():
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(setup_dir, 'README.rst')
    return open(filename).read().decode('utf8')

setup(
    name='django-privat24',
    version='0.1',

    packages=['privat24'],
    include_package_data=True,

    url='https://github.com/freshlimestudio/django-privat24',
    license = 'MIT License',
    description = 'PRIVAT24 payment system integration.',
    long_description = get_long_desc(),
    author='Igor Nephedov',
    author_email='igonef@pisem.net',
    install_requires=[
        'django>=1.5',
        'pyOpenSSL>=0.13.1',
    ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # example license
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Russian',
    ),
)
