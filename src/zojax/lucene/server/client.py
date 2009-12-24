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
""" zope lucene client interfaces

$Id$
"""

import xmlrpclib
from zope import interface
from interfaces import ILuceneClient


class LuceneClient(object):
    interface.implements(ILuceneClient)

    def __init__(self, name, url):
        self.url = url
        self.name = name
        self.connection = None

    def stop(self):
        self.connection = None

    def start(self):
        self.connection = xmlrpclib.ServerProxy(self.url)

    def __str__(self):
        return 'LuceneClient<%s,url=%s>'%(self.name, self.url)

    def __getattr__(self, name):
        return getattr(self.connection.lucene, name)
