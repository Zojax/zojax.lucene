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
""" zope lucene server implementation

$Id$
"""

import xmlrpclib, signal, os, os.path, copy
from subprocess import Popen

from zope import interface
from interfaces import ILuceneServer

dir = os.path.dirname(__file__)

classpath = []
for jar in ('lucene-core-2.2.0.jar', 'lucene-queries-2.2.0.jar',
            'lucene-snowball-2.2.0.jar', 'xmlrpc-1.2-b1.jar'):
    classpath.append(os.path.join(dir, 'jar', jar))

CLASSPATH = ':'.join(classpath)
SCRIPT = os.path.join(dir, 'indexserver.py')


class LuceneServer(object):
    interface.implements(ILuceneServer)

    def __init__(self, name, port, fspath, jython='/usr/bin/jython'):
        self.port = port
        self.name = name
        self.fspath = fspath
        self.jython = jython
        self.connection = None

    def stop(self):
        self.connection = None
        os.kill(self.proc.pid, signal.SIGTERM)

    def start(self):
        dir = os.path.dirname(__file__)

        env = copy.copy(os.environ)
        env['CLASSPATH'] = CLASSPATH

        self.proc = Popen([self.jython, SCRIPT, self.port, self.fspath], env=env)
        self.connection = xmlrpclib.ServerProxy('http://127.0.0.1:%s/lucene/'%self.port)

    def __str__(self):
        return 'LuceneServer<%s,port=%s>'%(self.name, self.port)

    def __getattr__(self, name):
        return getattr(self.connection.lucene, name)
