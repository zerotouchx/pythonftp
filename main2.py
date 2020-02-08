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
  if (_MD5 == True):
    md5hash = hashlib.md5()
  for root, dirs, files in os.walk(_SRC_PATH):  
    for fname in files:
      if fname == "main.py":
        continue
      else:
        if (_MD5):
          md5hash.update(fname)
          src_file[fname] = md5hash.hexdigest()
        else:
          src_file[fname] = None
  return src_file


def get_remote_files_info(_DEST_PATH, _MD5):
  _dirs = []
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
  for _fname in _dest_file.keys(): 
    if not _fname in _src_file: 
      _files_to_be_downloaded.append(_fname) 
  return _files_to_be_downloaded


##################################################################################################
def downlad_file(_SRC_PATH, _DEST_PATH, _SITE, _USERNAME, _PASSWORD, _FILES):
  count = 0
  ftp = login(_SITE, _USERNAME, _PASSWORD)
  ftp.cwd(_DEST_PATH)
  for _fname in _FILES:
    print("Downloading file: %s" % (_fname))
    ftp.retrbinary('RETR ' + fname, open(_SRC_PATH + '/' + _fname, 'wb').write)
    count += 1
  print("%d of Files have been downloaded" % (count))
  ftp.quit()

##################################################################################################

ftp = login(SITE, USERNAME, PASSWORD)

src_file = get_local_files_info(SRC_PATH, source_ldap_checksum)
dest_file = get_remote_files_info (DEST_PATH, source_ldap_checksum)
files_to_be_downloaded = calculate_diff(src_file, dest_file, source_ldap_checksum)


print (files_to_be_downloaded)


#print (get_local_files_info(SRC_PATH, source_ldap_checksum))
#print (get_remote_files_info(DEST_PATH, source_ldap_checksum))












