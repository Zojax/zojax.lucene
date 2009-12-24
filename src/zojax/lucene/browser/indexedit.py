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
from zope.formlib import form

from zojax.lucene.i18n import _
from zojax.lucene.interfaces import ILuceneIndex


class LuceneConfiguration(form.EditForm):

    form_fields = form.Fields(ILuceneIndex, render_context=True)

    label = _(u'Lucene Text Index')
    description = _(u'Using lucene text search engine '\
                        'for full text searching.')
