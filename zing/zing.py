#!/usr/bin/python
from StringIO import StringIO
import gzip
import urllib2
import html5lib
from html5lib import treebuilders, treewalkers, serializer

request = urllib2.Request('http://mp3.zing.vn/album/Yanni-Voices-Yanni/ZWZAUCEO.html')
request.add_header('Accept-encoding', 'gzip')
response = urllib2.urlopen(request)
if response.info().get('Content-Encoding') == 'gzip':
    print('Is gzip')
    buf = StringIO( response.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()
    #print(data)
else:
	print("Is not gzip")
	data = response.read()

parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
tree = parser.parse(data)
treeWalker = treewalkers.getTreeWalker("dom")
stream = treeWalker(tree)
#for token in stream:
#	print token
#serial = serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False)
#output = serial.serialize(stream)
#print(type(output))
#for element in output:
#	print(element)

#{'namespace': u'http://www.w3.org/1999/xhtml', 'type': 'StartTag', 'name': u'a', 'data': {(None, u'href'): u'http://mp3.zing.vn/download/song/Noi-Ay-Ha-Okio/ZHxHykHsSHVBWFRyLbJtFmkG', (None, u'title'): u'Download N\u01a1i \u1ea4y - H\xe0 Okio', (None, u'class'): u'music-download _btnDownload', (None, u'target'): u'_ifrTemp', (None, u'rel'): u'/downloads/song/Noi-Ay-Ha-Okio/128'}}
list_song = []

for token in stream:
    if(token.has_key('name') and token.has_key('data') and token['type'] == 'StartTag'):
    	if(token['name'] == 'a' and token['data']):
    		ldata = token['data']
    		if(ldata.has_key((None, 'class')) and ldata[(None, 'class')].find('music-download') != -1 and ldata[(None, 'class')].find('_btnDownload') != -1):
    			#print(ldata)
    			list_song.append(ldata[(None, 'href')])

print("Got " + str(len(list_song)) + " songs from the album")
for link in list_song:
	print(link)
    		