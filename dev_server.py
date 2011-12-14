import os
import sys
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import mimetypes
import glob
import hashlib

import generate
import config

file_hashes = {}

def check_hashes():
	modified = False
	for f in glob.glob(os.path.join(config.get("sourcedir"), "*.md")):
		md5 = hashlib.md5()
		md5.update(open(f, 'rb').read())
		h = md5.hexdigest()
		if file_hashes[f] != h:
			file_hashes[f] = h
			modified = True
	if modified:
		print "regenerating"
		generate.generate()

class SsgDevServer(BaseHTTPRequestHandler):

	def do_GET(self):
		check_hashes()
		if self.path[-1] == '/':
			self.path += 'index.html'
		try:
			servedir = config.get("servedir", config.get("outputdir"))
			f = open(os.path.join(servedir, self.path[1:]), "rb")
			self.send_response(200)
			filetype, _ = mimetypes.guess_type(self.path)
			self.send_header('Content-type', filetype)
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
		except IOError:
			self.send_error(404, "File not found: %s" % self.path)

def serve():
	for f in glob.glob(os.path.join(config.get("sourcedir"), "*.md")):
		md5 = hashlib.md5()
		md5.update(open(f, 'rb').read())
		file_hashes[f] = md5.hexdigest()
	try:
		srv = HTTPServer(("", 9876), SsgDevServer)
		print "Serving on localhost:9876"
		srv.serve_forever()
	except KeyboardInterrupt:
		srv.socket.close()
		sys.exit(0)

