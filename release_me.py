#!/usr/bin/python

import subprocess

def generate_release ():
  commands = (
    "git tag -a v%(version)s -m 'version %(version)s'",
    "git push --tags",
    "cd ..; tar cvf Church-Source_v%(version)s.tar Church-Source --exclude \"Church-Source/.git\"",
    "cd ..; gzip -9 Church-Source_v%(version)s.tar",
  )
  
  v = raw_input("Enter Version Number: ")
  
  for c in commands:
    print c % {'version': v}
    p = subprocess.Popen(c % {'version': v}, shell=True)
    sts = os.waitpid(p.pid, 0)[1]
    
if __name__ == '__main__':
  generate_release()
  