#!/bin/sh

# Path to the Jython startup script
JYTHON=/usr/bin/jython
 
# Index Data directory
INDEX=./indexdata

# XML-RPC Server Port
PORT=19980

# Path to the Lucene library
LUCENE=./jar/lucene-core-2.2.0.jar:./jar/lucene-queries-2.2.0.jar:./jar/lucene-snowball-2.2.0.jar
 
# Path to the XML-RPC library
XMLRPC=./jar/xmlrpc-1.2-b1.jar

export CLASSPATH=$LUCENE:$XMLRPC

# Start the server
$JYTHON indexserver.py $PORT $INDEX
