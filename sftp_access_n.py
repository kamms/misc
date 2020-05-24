import pysftp
import os
import json

conninfo = {'host': '192.168.1.195', 'port':222, 'username': 'FTP_scripter',\
            'private_key':os.path.join('~', '.ssh','FTP_scripter','id_rsa')}
with open('connection_properties.txt','w') as fil:
    json.dump(conninfo, fil)

with open('connection_properties.txt') as fil:
    conninfo = json.load(fil)


with pysftp.Connection(**conninfo) as sftp:
    sftp.put('initialization_steps.txt')
    print(sftp.pwd)

exit(0)
#with pysftp.Connection(host, username=user, private_key=keypath) as sftp:
    # temporarily chdir to public
#    with sftp.cd('public'):
        # upload file to public/ on remote
#        sftp.put('/my/local/filename')
    # recursively copy myfiles/ to local
#    sftp.get_r('myfiles', '/backup')

#with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
    #print("Connection succesfully stablished ... ")

    # Define the file that you want to upload from your local directorty
    # or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
#    localFilePath = './TUTORIAL2.txt'
    # Define the remote path where the file will be uploaded
    #remoteFilePath = '/var/integraweb-db-backups/TUTORIAL2.txt'

    #sftp.put(localFilePath, remoteFilePath)
# connection closed automatically at the end of the with-block
