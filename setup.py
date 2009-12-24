##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zojax.lucene package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.1.4'


setup(name='zojax.lucene',
      version=version,
      description="Lucene zope index",
      long_description=(
          'Detailed Dcoumentation\n' +
          '======================\n'
          + '\n\n' +
          read('src', 'zojax', 'lucene', 'README.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      author='Nikolay Kim',
      author_email='fafhrd91@gmail.com',
      url='http://zojax.net/',
      license='ZPL 2.1',
      package_dir = {'':'src'},
      packages=find_packages('src'),
      namespace_packages=['zojax'],
      install_requires = ['setuptools',
                          'zope.component',
                          'zope.interface',
                          'zope.publisher',
                          'zope.schema',
                          'zope.proxy',
                          'zope.index',
                          'zope.i18nmessageid',
                          'zope.app.twisted',
                          'zope.app.intid',
                          'zope.app.appsetup',
                          'zope.app.pagetemplate',
                          'zope.app.container',
                          'zope.app.catalog',
                          ],
      extras_require = dict(test=['zope.traversing',
                                  'zope.app.testing',
                                  'zope.testing',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
