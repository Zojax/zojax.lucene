# -*- coding: utf-8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# * Author: Nikolay Kim <fafhrd91@gmail.com>
""" zope lucene server/client interfaces

$Id$
"""

from zope import interface

class ILucene(interface.Interface):
    """ lucene server/client """

    name = interface.Attribute('Name')

    def stop(self):
        """ stop lucene """

    def start():
        """ start lucene """

    def __str__():
        """ """

class ILuceneClient(ILucene):
    """ client """

    URL = interface.Attribute('Server URL')


class ILuceneServer(ILucene):
    """ server """

    port = interface.Attribute('Port')
    fspath = interface.Attribute('Filesystem directory path')
