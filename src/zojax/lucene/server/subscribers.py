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
import logging
from twisted.internet import reactor

from zope import component
from zope.component import getGlobalSiteManager
from zope.app.appsetup.product import getProductConfiguration
from zope.app.appsetup.interfaces import IDatabaseOpenedEvent

from interfaces import ILucene
from client import LuceneClient
from server import LuceneServer


@component.adapter(IDatabaseOpenedEvent)
def startLucene(event):
    config = getProductConfiguration('zojax.lucene')
    if config is None:
        return

    jython = config.get('jython', '/usr/bin/jython')

    sm = getGlobalSiteManager()

    for name, data in config.items():
        data = [s.strip() for s in data.split(',')]

        if name.startswith('server'):
            lucene = LuceneServer(*data, **{'jython': jython})
        elif name.startswith('client'):
            lucene = LuceneClient(*data)
        else:
            continue

        try:
            lucene.start()
            sm.registerUtility(lucene, ILucene, data[0])
        except Exception, e:
            logging.getLogger('zojax.lucene').log(logging.WARNING, e)

    reactor.addSystemEventTrigger('before', 'shutdown', stopLucene)


def stopLucene():
    # stop all registered lucene
    sm = getGlobalSiteManager()

    for name, utility in sm.getUtilitiesFor(ILucene):
        utility.stop()
