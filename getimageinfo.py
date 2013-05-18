#!/usr/bin/python

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import time
import sys
import getopt
import re

from HTMLParser import HTMLParser




# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

	last_attrs=[]

	def handle_starttag(self, tag, attrs):
		self.last_attrs=attrs
	def handle_data(self, data):
		if(data.find('Visually similar')>=0):
			for i,v in self.last_attrs:
				if( i.find('href')>=0 ):
					question = v[v.find('q=')+2:]
					end_of_question = question.find('&')
					print question[:end_of_question].replace('+',' ')
					sys.exit(0)

def get_image_info(filename):
	# Register the streaming http handlers with urllib2
	register_openers()

	datagen, headers = multipart_encode({"image_url":"","btnG":"Search","image_content":"","filename":"","hl":"en","safe":"off","bih":"", "biw":"", "encoded_image": open(filename, "rb")})

	headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0'
	headers['Referer']='http://images.google.com'
	headers['Accept']='*/*'
	headers['Accept-Encoding']=''
	headers['Connection']='Keep-Alive'
	headers['Expect']='100-continue'	

	# Create the Request object
	request = urllib2.Request("http://www.google.com/searchbyimage/upload", datagen, headers)
	# Actually do the request, and get the response
	response = urllib2.urlopen(request).read()
	
	# instantiate the parser and fed it some HTML
	parser = MyHTMLParser()
	
	parser.feed(response)
	
	
def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:",["ifile="])
	except getopt.GetoptError:
		print 'getimageinfo -i <inputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'getimageinfo.py -i <inputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
	
	get_image_info(inputfile)

if __name__ == "__main__":
	main(sys.argv[1:])
