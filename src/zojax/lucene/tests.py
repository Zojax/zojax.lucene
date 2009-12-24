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
""" zojax.lucene tests

$Id$
"""
__docformat__ = "reStructuredText"

import os, sys
import unittest, doctest
from zope import interface, schema
from zope.component import provideAdapter
from zope.app.testing import setup
from zope.traversing.namespace import view
from zope.traversing.interfaces import ITraversable

from zojax.lucene.server.subscribers import stopLucene

JYTHON = '/usr/bin/jython'


def setUp(test):
    setup.placelessSetUp()


def tearDown(test):
    stopLucene()
    setup.placelessTearDown()

def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite(
                'README.txt',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))
