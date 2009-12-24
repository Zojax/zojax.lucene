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

from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from zojax.lucene.utils import indexObject
from zojax.lucene.interfaces import ILuceneIndex


class IndexView(object):

    def __call__(self):
        self.update()
        return self.index()

    def getStatistics(self):
        index = self.context
        
        try:
            return {'documents': index.documentCount(),
                    'words': index.wordCount()}
        except:
            return {'documents': 'Unknown', 'words': 'Unknown'}

    def update(self):
        request = self.request

        if request.has_key('advanced.reindexAll'):
            intids = getUtility(IIntIds)
            index = getUtility(ILuceneIndex)

            for id in intids:
                ob = intids.queryObject(id)
                if ob is not None:
                    indexObject(ob, index, intids)
