#!/usr/bin/python3
import requests
import zipfile
import io
import yaml
import sys
import os
import urllib.request
import platform
import tarfile


VERSION = "0.12.5"

LINUX_URL  = "https://github.com/rancher/rancher-compose/releases/download/v"+ VERSION + "/"
LINUX_FILENAME = "rancher-compose-linux-amd64-v"+ VERSION

WINDOWS_URL  = "https://github.com/rancher/rancher-compose/releases/download/v"+ VERSION + "/"
WINDOWS_FILENAME = "rancher-compose-windows-amd64-v"+ VERSION

if len (sys.argv) < 6:
    print("ISH Labs - Rancher-Composer")
    print("Usage: " + sys.argv[0] + " URL_COMPOSECONFIG USER_API SECRET_API ENVIROMENT_NAME SERVICE_NAME")
    print("Example: " + sys.argv[0] + " https://rancher.server/v2-beta/projects/1a23711/stacks/1st294/composeconfig CF175922F68B31AA54C9 We8UTQ7Ky2VtEzhKOakq9bhCUWKE3gYvmPSZQa4A MyEnviroment app01")
    sys.exit (1)

RURLAPI     = sys.argv[1]
RUSER       = sys.argv[2]
RPASS       = sys.argv[3]
RENVNAME = sys.argv[4]
RSERVICE = sys.argv[5]

try:
    os.remove('rancher-compose.yml')
    os.remove('docker-compose.yml')
    os.remove('rancher-compose.tmp')
    os.remove('docker-compose.tmp')
    os.remove('docker-compose.tmp')
except OSError:
    pass

if platform.system() == 'Linux':
    urllib.request.urlretrieve(LINUX_URL + LINUX_FILENAME + '.tar.gz', LINUX_FILENAME + '.tar.gz')
    tar = tarfile.open(LINUX_FILENAME + ".tar.gz", "r:gz")
    tar.extractall()
    tar.close()
    COMPOSEPATH = "./rancher-compose-v" + VERSION + "/rancher-compose"

if platform.system() == 'Windows':
    urllib.request.urlretrieve(WINDOWS_URL + WINDOWS_FILENAME + '.zip', WINDOWS_FILENAME + '.zip')
    z = zipfile.ZipFile(WINDOWS_FILENAME + '.zip')
    z.extractall()
    COMPOSEPATH = ".\\rancher-compose-v" + VERSION + "\\rancher-compose.exe"


r = requests.get(RURLAPI, stream=True, auth=(RUSER, RPASS))
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

##############
with open('docker-compose.yml', 'r') as f:
    doc = yaml.load(f)

dockercomposer = yaml.dump(doc["services"][RSERVICE])

with open('docker-compose.yml', 'w') as file:
    file.write(RSERVICE + ':\n' + dockercomposer)

with open('docker-compose.yml', 'r') as fp:
    q = 0
    with open('docker-compose.tmp', 'a') as file:
        file.write(RSERVICE + ':\n')
        for line in fp:
            q = q + 1
            if q > 1:
                file.write(' ' + line)

os.remove('docker-compose.yml')
os.rename('docker-compose.tmp', 'docker-compose.yml')

################

with open('rancher-compose.yml', 'r') as f:
    doc = yaml.load(f)

dockercomposer = yaml.dump(doc["services"][RSERVICE])

with open('rancher-compose.yml', 'w') as file:
    file.write(RSERVICE + ':\n' + dockercomposer)

with open('rancher-compose.yml', 'r') as fp:
    q = 0
    with open('rancher-compose.tmp', 'a') as file:
        file.write(RSERVICE + ':\n')
        for line in fp:
            q = q + 1
            if q > 1:
                file.write(' ' + line)

os.remove('rancher-compose.yml')
os.rename('rancher-compose.tmp', 'rancher-compose.yml')

print(COMPOSEPATH +
      " --url " + RURLAPI +
      " --access-key " + RUSER +
      " --secret-key " + RPASS +
      " --project-name " + RENVNAME +
      " --file docker-compose.yml " +
      " --rancher-file rancher-compose.yml up -d" +
      " --batch-size 1" +
      " --confirm-upgrade" +
      " --pull" +
      " --force-upgrade " + RSERVICE)

os.system(COMPOSEPATH +
      " --url " + RURLAPI +
      " --access-key " + RUSER +
      " --secret-key " + RPASS +
      " --project-name " + RENVNAME +
      " --file docker-compose.yml " +
      " --rancher-file rancher-compose.yml up -d" +
      " --batch-size 1" +
      " --confirm-upgrade" +
      " --pull" +
      " --force-upgrade " + RSERVICE)

