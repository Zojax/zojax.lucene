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
""" zojax.lucene interfaces

$Id$
"""
from zope import schema, interface
from zope.index.interfaces import IInjection, IIndexSearch, IStatistics

from i18n import _
from vocabulary import languages


class ILuceneIndex(IInjection, IIndexSearch, IStatistics):
    """This is a general interface for indexes that use remote engines
    to index documents, such as Lucene."""
 
    utility = schema.Choice(
        title=_(u'Lucene Server'),
        description=_(u'Select configured lucene server.'),
        vocabulary='zojax.lucene.servers',
	missing_value=u'',
        required=False)

    language = schema.Choice(
        title=_(u'Default language'),
        description=_(u'Select default language of indexed text.'),
        default='English',
        vocabulary=languages,
        required = False)

    def connect():
        """Connect to the server."""

    def disconnect():
        """Disconnect from the server."""


class ILuceneProduct(interface.Interface):
    """ lucene configuration interface """
