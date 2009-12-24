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
""" installer for zojax.poduct

$Id$
"""
from zope import interface
from zope.app.catalog.interfaces import ICatalogIndex

from zojax.product.utils import registerUtility, unregisterUtility

from zojax.lucene.i18n import _
from zojax.lucene.interfaces import ILuceneIndex, ILuceneProduct

from zojax.lucene.index import BaseLuceneTextIndex


class PortalLuceneIndex(BaseLuceneTextIndex):
    """ portal index """


class LuceneInstaller(object):
    interface.implements(ILuceneProduct)

    def update(self):
        registerUtility('zojax.lucene', PortalLuceneIndex,
                        ((ILuceneIndex, ''), 
                         (ICatalogIndex, 'searchableText')))
        super(LuceneInstaller, self).update()

    def uninstall(self):
        unregisterUtility('zojax.lucene',
                          ((ILuceneIndex, ''), (ICatalogIndex, 'searchableText')))
        super(LuceneInstaller, self).uninstall()
