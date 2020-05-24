import pysftp
import os
import json
import sys

with open('connection_properties.txt') as fil:
    conninfo = json.load(fil)

with pysftp.Connection(**conninfo) as sftp:
    sftp.chdir('FTP')
    sftp.put(sys.argv[1])
