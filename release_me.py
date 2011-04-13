#!/usr/bin/python

import os
import sys
import subprocess
import argparse

def run_commands (v, cmds):
  for c in cmds:
    print c % {'version': v}
    p = subprocess.Popen(c % {'version': v}, shell=True)
    sts = os.waitpid(p.pid, 0)[1]
    
def generate_release ():
  parser = argparse.ArgumentParser(description='Generate Church Source release')
  parser.add_argument('-g', help='Tag Release with Git', action='store_true')
  parser.add_argument('-t', help='Generate Tarball', action='store_true')
  args = parser.parse_args()
  
  git_commands = (
    "git tag -a v%(version)s -m 'version %(version)s'",
    "git push --tags",
  )
  
  tar_commands = (
    "cd ..; tar cvf Church-Source_v%(version)s.tar Church-Source --exclude *.pyc --exclude Church-Source/.git --exclude Church-Source/.gitignore --exclude Church-Source/release_me.py --exclude Church-Source/playground --exclude Church-Source/churchsource/static/uploads --exclude Church-Source/churchsource/static/cache --exclude Church-Source/churchsource/settings_local.py",
    "cd ..; gzip -9 Church-Source_v%(version)s.tar",
  )
  
  v = raw_input("Enter Version Number: ")
  
  if args.g:
    for c in git_commands:
      run_commands(v, git_commands)
      
  if args.t:
    for c in tar_commands:
      run_commands(v, tar_commands)
      
if __name__ == '__main__':
  generate_release()
  