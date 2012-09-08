import subprocess
import os

'''
@class BackupJob
@author tom@0x101.com

A BackupJob is a Command pattern approach for running external
programs that will generate the filename that we need in order
to have a backup package.

They are defined based on the following parameters
	"script": "gd1.sh",
	"filename": "gd1.tar.gpg"
	"folder": "./jobs/"

In the previous example, BackupJob will search the external
script in './jobs/gd1.sh' and once executed will place a file
called "gd1.tar.gpg" in the same folder.
'''
class BackupJob:

   script = None
   filename = None
   path = None

   def __init__(self, folder, script, filename):
      self.path = self.__getPath__(folder)
      self.filename = self.path + filename
      self.script = script

   def __getPath__(self, folder):
      return os.getcwd() + '/' + folder + '/'

   '''
   Remove files from previous jobs.
   '''
   def clean(self):
      if os.path.exists(self.filename):
         os.remove(self.filename)

   def run(self):

      self.clean()
      subprocess.call([self.path + '/' + self.script], shell = True, cwd = self.path)

      if not os.path.exists(self.filename):
         raise BackupJobException()

      return self.filename

'''
General purpose exception for the BackupJob class.
'''
class BackupJobException(Exception):
   pass
