#!/usr/bin/jython
# -*- coding: utf-8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# * Author: Nikolay Kim <fafhrd91@gmail.com>
""" lucene index server implementation

$Id$
"""

import os, sys, time

from java.util import Vector

from org.apache.xmlrpc import WebServer, XmlRpcHandler

from org.apache.lucene.document import Document, Field
from org.apache.lucene.analysis import StopAnalyzer, SimpleAnalyzer
from org.apache.lucene.index import IndexReader, IndexWriter, Term
from org.apache.lucene.search import IndexSearcher, Hits, BooleanClause
from org.apache.lucene.search import BooleanFilter, RangeFilter, FilterClause

from org.apache.lucene.store import FSDirectory
from org.apache.lucene.queryParser import QueryParser
 
# Jython is not yet Python 2.2 compatible.
True = 1
False = 0

def log(msg='', subsystem='lucene indexserver'):
    #log = logging.getLogger(subsystem)
    #log.log(logging.INFO, msg)
    #print msg
    pass

 
class LuceneXMLRPCHandler(XmlRpcHandler):

    def __init__(self, indexPath):
        """Instantiate the handler object."""
        self.indexPath = indexPath
        self.analyzer = StopAnalyzer()
        
        # Make sure the path exists
        if not os.path.exists(self.indexPath):
            os.mkdir(self.indexPath)

        if not os.path.exists(os.path.join(self.indexPath, 'segments.gen')):
            log('Creating new index.')
            writer = IndexWriter(self.indexPath, self.analyzer, 1)
            writer.close()

    def execute(self, name, args):
        """See interface XmlRpcHandler."""
        if name.startswith('lucene.'):
            name = name[7:]
        return getattr(self, 'xmlrpc_'+name)(*args)

    def xmlrpc_unindexDocument(self, instance, id):
        """ Unindex document """
        filter = BooleanFilter()

        filter.add(FilterClause(RangeFilter('id', id, id, 1, 1),
                                BooleanClause.Occur.MUST))
        filter.add(FilterClause(RangeFilter('instance', instance, instance, 1, 1),
                                BooleanClause.Occur.MUST))
        
        reader = IndexReader.open(self.indexPath)

        bits = filter.bits(reader)

        docId = bits.nextSetBit(0)
        while docId >= 0:
            reader.deleteDocument(docId)
            docId = bits.nextSetBit(docId+1)

        reader.close()

    def xmlrpc_indexDocument(self, instance, id, text):
        """Index a new document."""
        self.xmlrpc_unindexDocument(instance, id)

        # Create a document and add two fields to it. 
        doc = Document()
        doc.add(Field('id', id, Field.Store.YES, Field.Index.UN_TOKENIZED))
        doc.add(Field('text', text, Field.Store.YES, Field.Index.TOKENIZED))
        doc.add(Field('instance', instance, Field.Store.YES, Field.Index.UN_TOKENIZED))

        # Write the document into the index.
        writer = IndexWriter(self.indexPath, self.analyzer, 0)
        writer.addDocument(doc)
        writer.optimize()
        writer.close()
        log('Insert: Instance: %s Document: %s' %(instance, id))
        return 1

    def xmlrpc_query(self, instance, querytext):
        """Query the index."""
        query = QueryParser('text', self.analyzer)
        log('Instance: %s, Query: %s' %(instance, querytext))
         
        searcher = IndexSearcher(self.indexPath)
        results = searcher.search(query.parse(querytext),
                                  RangeFilter('instance', instance, instance, 1, 1))

        # Prepare the result for XML-RPC.
        ids = Vector()
        for hitid in range(results.length()):
            entry = Vector()
            entry.add(results.doc(hitid).getField('id').stringValue())
            entry.add(results.score(hitid))
            ids.add(entry)
 
        return ids

    def xmlrpc_getStatistics(self, instance):
        reader = IndexReader.open(self.indexPath)

        filter = RangeFilter('instance', instance, instance, 1, 1)

        num = filter.bits(reader).cardinality()

        stat = Vector()
        stat.add(num)
        stat.add(0)#len(index.terms()))
        reader.close()
        return stat


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'usage: indexserver.py port index_dir'
        sys.exit(1)
 
    web = WebServer(int(sys.argv[1]))
    web.addHandler('lucene', LuceneXMLRPCHandler(sys.argv[2]))
    log('Starting Lucene XML-RPC Server on port %s' %sys.argv[1])
    web.start()
