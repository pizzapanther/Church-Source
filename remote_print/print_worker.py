#!/usr/bin/python

import os
import sys
import time
import urllib
import traceback
import subprocess

import simplejson

from PIL import Image, ImageFont, ImageDraw

SFILE = __file__
SPATH = os.path.normpath(os.path.dirname(SFILE))

sys.path.insert(0, SPATH)

font_path = os.path.join(SPATH, 'Ubuntu-Regular.ttf')

import daemon

def print_worker (url):
  font1 = ImageFont.truetype(font_path, 25)
  
  try:
    fh = urllib.urlopen(url)
    data = fh.read()
    fh.close()
    
  except:
    traceback.print_exc()
    
  else:
    
    data = simplejson.loads(data)
    for key, value in data.items():
      for ci in value:
        img = Image.new('RGB', (400, 300), '#fff')
        draw = ImageDraw.Draw(img)
        
        draw.text((10, 25), ci['fname'] + ' ' + ci['lname'], font=font1, fill='#000')
        
        img.save('/tmp/checkin.png', "PNG")
        #retcode = subprocess.call("lpr -P LP2844 /tmp/checkin.png", shell=True)
        
if __name__ == "__main__":
  if 'fg' in sys.argv:
    print_worker(sys.argv[1])
    
  else:
    with daemon.DaemonContext():
      print_worker(sys.argv[1])
      
