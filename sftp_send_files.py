import pysftp
import os
import json
import sys

connection_file = sys.argv[1]
files_to_send = sys.argv[2:]

with open(connection_file) as fil:
    conninfo = json.load(fil)

with pysftp.Connection(**conninfo) as sftp:
    sftp.chdir('FTP')
    for fname in files_to_send:
        sftp.put(fname)
