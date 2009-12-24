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
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


languages = SimpleVocabulary((
        SimpleTerm('Danish', 'Danish', 'Danish'),
        SimpleTerm('Dutch', 'Dutch', 'Dutch'),
        SimpleTerm('English', 'English', 'English'),
        SimpleTerm('Finnish', 'Finnish', 'Finnish'),
        SimpleTerm('French', 'French', 'French'),
        SimpleTerm('German', 'German', 'German'),
        SimpleTerm('Italian', 'Italian', 'Italian'),
        SimpleTerm('Norwegian', 'Norwegian', 'Norwegian'),
        SimpleTerm('Portuguese', 'Portuguese', 'Portuguese'),
        SimpleTerm('Russian', 'Russian', 'Russian'),
        SimpleTerm('Spanish', 'Spanish', 'Spanish'),
        SimpleTerm('Swedish', 'Swedish', 'Swedish')))
