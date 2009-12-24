=================
Lucene Text index
=================

Apache Lucene index for zope3. Jython is required.

For configure default settings, add following code to zope.conf

<product-config zojax.lucene>
  server1 testing server,8981,/path-to-lucene/Zope3/var/luceneindex
</product-config>

First server record, then parameters seperated by ','
First title of lucene server also this title is using for utility name,
port, directory where lucene should create it's data

We need temporary directory

   >>> import tempfile
   >>> lucene_dir = tempfile.mkdtemp()

We'll try emulate <product-config zojax.lucene> 

   >>> from zojax.lucene.tests import JYTHON
   >>> from zope.app.appsetup import product
   >>> product._configs['zojax.lucene'] = {'server1': \
   ...  'testing server,56999,%s'%lucene_dir, 'jython': JYTHON}

Let's check this

   >>> product.getProductConfiguration('zojax.lucene')
   {'jython': '...jython', 'server1': 'testing server,56999,...'}


Usually startLucene() function is colled during IDatabaseOpenedEvent event,
we simply call it directly:

   >>> from zojax.lucene.server.subscribers import startLucene
   >>> startLucene(None)

Lucene server registers in system as ILucene with name.

   >>> from zope.component import getUtility       
   >>> from zojax.lucene.server.interfaces import ILucene

   >>> server = getUtility(ILucene, 'testing server')
   >>> print server
   LuceneServer<testing server,port=56999>

We need give some time to lucene server to start

   >>> import time
   >>> time.sleep(5)

Now we need catalog index

   >>> from zojax.lucene.index import LuceneTextIndex

   >>> index = LuceneTextIndex('testing server')

   >>> from zope import interface
   >>> from zope.index.text.interfaces import ISearchableText

Indexed document you have ISearchableText adapter to get indexed.
We will create simple object that implements ISearchableText

   >>> class Document(object):
   ...    interface.implements(ISearchableText)
   ...    def __init__(self, text):
   ...       self.text = text
   ...    def getSearchableText(self):
   ...       return self.text

   >>> doc1 = Document(\
   ...   "A utility is registered to provide an interface with a "\
   ...   "name. If a component provides only one interface, then the"\
   ...   "provides argument can be omitted and the provided interface"\
   ...   "will be used. (In this case, provides argument can still be"\
   ...   "provided to provide a less specific interface.)")
   >>> doc2 = Document(\
   ...   "Return a list of adapters that match. If an adapter is named, "\
   ...   "only the most specific adapter of a given name is returned." \
   ...   "If context is None, an application-defined policy is used to choose "\
   ...   "an appropriate service manager from which to get an 'Adapters' service.")


Let's index documents

   >>> index.index_doc('1', doc1)
   >>> index.index_doc('2', doc2)

Now we can search text

   >>> list(index.apply('component provides'))
   [1]

   >>> list(index.apply('service manager'))
   [2]

   >>> list(index.apply('name'))
   [1, 2]


Statistics

   >>> index.documentCount(), index.wordCount()
   (2, 0)

We can use any number of Luxene indexes with one lucene server

   >>> index2 = LuceneTextIndex('testing server')

   >>> list(index2.apply('component provides'))
   []
   >>> list(index2.apply('service manager'))
   []
   >>> list(index2.apply('name'))
   []


ZEO setup
---------

With zeo setup we should run only one copy of Lucene Server. So we can start
lucene server on one zope instance (or by using 
zojax/lucene/server/server.sh script we can run lucene server anywhere)
and on other instances we can use LuceneClient

Configuration for zope.conf

<product-config zojax.lucene>
  client1 lucene client,http://127.0.0.1:56999/lucene/
</product-config>

   >>> from zope.component import provideUtility
   >>> from zojax.lucene.server.client import LuceneClient
   >>> client = LuceneClient('lucene client', 'http://127.0.0.1:56999/lucene/')
   >>> provideUtility(client, ILucene, 'lucene client')

   >>> index.utility = 'lucene client'

   >>> list(index.apply('component provides'))
   [1]

   >>> list(index.apply('service manager'))
   [2]

   >>> list(index.apply('name'))
   [1, 2]


unindex_doc
-----------

   >>> index.unindex_doc('2')
   >>> list(index.apply('service manager'))
   []

   >>> index.clear()