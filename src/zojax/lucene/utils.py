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
"""

$Id$
"""
from zope.component import queryUtility
from zope.app.intid.interfaces import IIntIds

from interfaces import ILuceneIndex


def indexObject(object, index=None, intids=None):
    if index is None:
        index = queryUtility(ILuceneIndex)

    if index is not None:
        if intids is None:
            intids = queryUtility(IIntIds)
            
        if intids is not None:
            id = intids.queryId(object)

            if id is not None:
                index.index_doc(id, object)


def unindexObject(object, index=None, intids=None):
    if index is None:
        index = queryUtility(ILuceneIndex)

    if index is not None:
        if intids is None:
            intids = queryUtility(IIntIds)

        if intids is not None:
            id = intids.queryId(object)

            if id is not None:
                index.unindex_doc(id)
