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
from zope.traversing.browser import absoluteURL
from zope.app.intid.interfaces import IIntIds
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.layoutform import Fields, PageletEditForm
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.lucene.i18n import _
from zojax.lucene.utils import indexObject
from zojax.lucene.interfaces import ILuceneIndex


class LuceneProduct(PageletEditForm):

    fields = Fields(ILuceneIndex)

    label = _(u'Lucene Text Index')
    description = _(u'Using lucene text search engine for full text searching.')

    info = ViewPageTemplateFile('product.pt')

    def getContent(self):
        return getUtility(ILuceneIndex)

    def getStatistics(self):
        index = getUtility(ILuceneIndex)

        try:
            return {'documents': index.documentCount(),
                    'words': index.wordCount()}
        except:
            return {'documents': 'Unknown', 'words': 'Unknown'}

    def update(self):
        super(LuceneProduct, self).update()

        request = self.request

        if request.has_key('advanced.reindexAll'):
            intids = getUtility(IIntIds)
            index = getUtility(ILuceneIndex)

            for id in intids:
                ob = intids.queryObject(id)
                if ob is not None:
                    indexObject(ob, index, intids)

            IStatusMessage(request).add(_(u'Reindex process has been completed.'))

    def render(self):
        rendered = super(LuceneProduct, self).render()

        return rendered + self.info()
