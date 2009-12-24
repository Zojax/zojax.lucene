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

from interfaces import ILucene
from zope.component import getUtilitiesFor
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


class Vocabulary(SimpleVocabulary):

    def getTerm(self, value):
        try:
            return super(Vocabulary, self).getTerm(value)
        except LookupError:
            return self._terms[0]


class LuceneVocabulary(object):

    def __call__(self, context):
        terms = []
        for name, utility in getUtilitiesFor(ILucene):
            terms.append((str(utility),
                          SimpleTerm(utility.name, utility.name, str(utility))))

        terms.sort()
        return Vocabulary([term for t, term in terms])
