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
""" index implementation

$Id$
"""
import sys, random, logging
from datetime import datetime
from persistent import Persistent
from BTrees.IFBTree import IFSet

from zope import interface
from zope.component import queryUtility, getAdapters

from zope.app.container.contained import Contained

from zope.app.catalog.interfaces import ICatalogIndex
from zope.index.text.interfaces import ISearchableText

from zojax.lucene.interfaces import ILuceneIndex
from zojax.lucene.server.interfaces import ILucene


class BaseLuceneTextIndex(Persistent, Contained):
    """Lucene Text Index."""
    interface.implements(ILuceneIndex)

    utility = ''
    language = 'English'

    _instance = None

    def __init__(self, utility=''):
        self.utility = utility

    @property
    def instance(self):
        id = self._instance
        if id is None:
            id = u'%010d-%s' % (random.randrange(sys.maxint), datetime.now().toordinal())
            self._instance = id
        return id

    def connect(self):
        if not hasattr(self, '_v_connection') or \
                self._v_connection is None:
            self._v_connection = queryUtility(ILucene, self.utility)
        return self._v_connection
 
    def disconnect(self):
        self._v_connection = None

    def clear(self):
        pass
 
    def index_doc(self, docid, obj):
        """See zope.textindex.textindexinterfaces.IInjection"""
        server = self.connect()
        if server is None:
            return

        text = []
        st = ISearchableText(obj, None)
        if st is not None:
            text.append(st.getSearchableText())

        for name, st in getAdapters((obj,), ISearchableText):
            text.append(st.getSearchableText())

        text = u' '.join(text)
        if text:
            try:
                server.indexDocument(self.instance, str(docid), text)
            except Exception, e:
                logging.getLogger('zojax.lucene').log(logging.WARNING, e)

    def unindex_doc(self, docid):
        """See zope.textindex.textindexinterfaces.IInjection"""
        server = self.connect()
        try:
            server.unindexDocument(self.instance, str(docid))
        except:
            pass

    def apply(self, querytext, start=0, count=None):
        """See zope.textindex.textindexinterfaces.IQuerying"""
        if type(querytext) is dict:
            if len(querytext) > 1:
                raise ValueError('may only pass one of key, value pair')
            elif not querytext:
                return None

            query_type, query = querytext.items()[0]
            query_type = query_type.lower()

            if isinstance(query, basestring):
                query = (query,)

            values = []
            for value in query:
                values.append(' AND '.join(unicode(value).split()))

            if query_type == 'any_of':
                querytext = ' OR '.join(values)
            elif query_type == 'all_of':
                querytext = ' AND '.join(values)
            else:
                return None

        server = self.connect()
        try:
            results = server.query(self.instance, querytext)
        except:
            return None

        return IFSet([int(x[0]) for x in results])

    def _getStatistics(self):
        if not hasattr(self, '_v_stats') or self._v_stats is None:
            server = self.connect()
            try:
                return server.getStatistics(self.instance)
            except:
                return [-1, -1]
            self._v_stats = server.getStatistics(self.instance)

        return self._v_stats

    def documentCount(self):
        """See zope.textindex.textindexinterfaces.IStatistics"""
        return self._getStatistics()[0]
    
    def wordCount(self):
        """See zope.textindex.textindexinterfaces.IStatistics"""
        return self._getStatistics()[1]


class LuceneTextIndex(BaseLuceneTextIndex):
    interface.implements(ICatalogIndex)
