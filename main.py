import ftplib
import hashlib
import sys
import os
import time
####################################################
__author__ = "Gokay Yildirim"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Gokay Yildirim"
__status__ = "Development"

####################################################
SITE = "192.168.122.232"
SRC_PATH = "/home/tesla/python/ftp/"
DEST_PATH = "/"
USERNAME = "ftp"
PASSWORD = "ftp"
src_file = {}
dest_file = {}
#if you do not want to 
source_ldap_checksum = True 
files_to_be_downloaded = []  
#################################################### 
#Checks the HW Platform as script only tried on GNU/Linux.
def uname ():
  if sys.platform.startswith('freebsd'):
    return "FREEBSD"
  elif sys.platform.startswith('linux'):
    return "LINUX"
  elif sys.platform.startswith('aix'):
    return "AIX"
  else: 
    return "UNKNOWN"

#Defining Login function
def login(_SITE, _USERNAME, _PASSWORD):
  _ftp = ftplib.FTP(_SITE)
  _ftp.login(_USERNAME, _PASSWORD)
  return _ftp


def get_local_files_info(_SRC_PATH, _MD5):
  _src_file = {}  
  for root, dirs, files in os.walk(_SRC_PATH):  
    for _fname in files:
      if _fname == "main.py":
        continue
      else:
        if (_MD5):
          md5hash = hashlib.md5()
          with open(_SRC_PATH + '/' + _fname, 'rb') as f:
            while True:
              data = f.read(8192)
              if not data:
                break
              md5hash.update(data)
            _src_file[_fname] = md5hash.hexdigest()
            #print ("LCAO", md5hash.hexdigest())

        else:
          _src_file[_fname] = None
  return _src_file


def get_remote_files_info(_DEST_PATH, _MD5):
  _dirs = []
  ftp.cwd(_DEST_PATH)
  ftp.retrlines('MLSD', _dirs.append)
  for line in  _dirs:
  #type=file;modify=20200204232150;size=3197; a.txt
    _type = line.split(';')[0].split('=')[1]
    _fname = line.split(';')[-1].strip()
    if (_type == "file"):
      if (_MD5):
        md5hash = hashlib.md5()
        dest_file[_fname] = ftp.retrbinary('RETR ' + _fname, md5hash.update )
        dest_file[_fname] = md5hash.hexdigest()
      else:
        dest_file[_fname] = None
  return dest_file  
#################################################################################################

def calculate_diff(_src_file, _dest_file, _MD5):
  _files_to_be_downloaded = []
  if (_MD5):
    for _fname in _dest_file.keys():
      if _fname in _src_file:
        if _src_file[_fname] != _dest_file[_fname]:
          print("Existing file has changed: %s" % (_fname))
          _files_to_be_downloaded.append(_fname)
          #print (_src_file[_fname], _fname)
          #print (_dest_file[_fname], _fname)
  for _fname in _dest_file.keys(): 
    if not _fname in _src_file: 
      print("New file has been added: %s" % (_fname))
      _files_to_be_downloaded.append(_fname) 

  return _files_to_be_downloaded


##################################################################################################
def downlad_file(_SRC_PATH, _DEST_PATH, _FILES):
  count = 0
  #ftp = login(_SITE, _USERNAME, _PASSWORD)
  ftp.cwd(_DEST_PATH)
  for _fname in _FILES:
    print("Downloading file: %s" % (_fname))
    ftp.retrbinary('RETR ' + _fname, open(_SRC_PATH + '/' + _fname, 'wb').write)
    count += 1
  if (count == 0):
    print("No files to be downloaded, SYNCED")
  else:
    print("%d of Files have been downloaded" % (count))
  ftp.quit()

##################################################################################################

if (uname() == "LINUX"):
  ftp = login(SITE, USERNAME, PASSWORD)
  src_file = get_local_files_info(SRC_PATH, source_ldap_checksum)
  dest_file = get_remote_files_info (DEST_PATH, source_ldap_checksum)
#Debugging purpose.
  #print (get_local_files_info(SRC_PATH, source_ldap_checksum))
  #print (get_remote_files_info(DEST_PATH, source_ldap_checksum))
  files_to_be_downloaded = calculate_diff(src_file, dest_file, source_ldap_checksum)
  #print("Files to be downloaded: %s" % (files_to_be_downloaded))
#This function download the files on the remote Site. if you are not sure what to do
#comment it and uncomment the debug lines.
  downlad_file(SRC_PATH, DEST_PATH, files_to_be_downloaded)
else:
  print("System tested only GNU/Linux distribution.")
  print("Abort...")
  sys.exit(1)















