import os
import sys
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import mimetypes

import config

class SsgDevServer(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			serve_dir = config.get("serve_dir", config.get("output_dir"))
			f = open(os.path.join(serve_dir, self.path[1:]), "rb")
			self.send_response(200)
			filetype, _ = mimetypes.guess_type(self.path)
			self.send_header('Content-type', filetype)
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
		except IOError:
			self.send_error(404, "File not found: %s" % self.path)

def serve():
	try:
		srv = HTTPServer(("", 9876), SsgDevServer)
		print "Serving on localhost:9876"
		srv.serve_forever()
	except KeyboardInterrupt:
		srv.socket.close()
		sys.exit(0)

