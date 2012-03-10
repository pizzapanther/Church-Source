#!/usr/bin/python

import BaseHTTPServer
import SocketServer

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import time

PORT = 8000

class Handler (BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET (self):
    self.send_head()
    if self.path == '/print/':
      browser = webdriver.Firefox(firefox_profile='/home/paul/Documents/sel/')
      browser.get("http://10.74.193.240/checkin/printjobs/")
      time.sleep(15)
      browser.close()
      
    self.wfile.write("1\n")
    
  def send_head(self):
    self.send_response(200)
    self.send_header("Content-type", 'application/javascript')
    self.end_headers()
    return None
    
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

#>>> from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#>>> p = FirefoxProfile(profile_directory='/home/paul/Documents/sel/')
#>>> from selenium import webdriver
#>>> p.set_preference('print.postscript.orientation', 'landscape')
#>>> browser = webdriver.Firefox(firefox_profile=p)
