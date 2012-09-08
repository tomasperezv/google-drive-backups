import sqlite3
from datetime import date

'''
@class DataBaseBackup
@author tom@0x101.com

Stores the backups in a database, using a basic schema. The current engine is based on
sqlite3. If it needs other engines in the future, then the database engine logic would need to be
moved from here.

The logic that determines if we need to store a backup for a specific project, is based on the current
timestamp and only stores one backup per day as the schema it uses is 'ddmmyyyy'. Other aproaches would
need to modify the method 'pending' and 'getCurrentId' that encapsulate that logic.
'''
class DataBaseBackup:

   '''
   Connection to the sqlite3 database
   '''
   connection = None

   '''
   In a dry run mode, it won't commit the queries.
   '''
   dryRun = False

   def __init__(self, database, dryRun = False):
      self.database = database
      self.dryRun = dryRun

   '''
   Check if we need to create and store a new backup.
   Simple process, get the id that corresponds to the current date,
   and check if we have already an entry in the database.
   '''
   def pending(self, projectId):
      if self.connection is None:
         self.__connect__()
      currentId = self.getCurrentId()
      result = self.connection.execute('SELECT * FROM backups WHERE timestamp = "' + currentId + '" AND project_id = "' + projectId + '"')
      return result.fetchone() is None

   '''
   Add a new entry in the backup database.
   '''
   def add(self, projectId):
      if self.connection is None:
         self.__connect__()
      currentId = self.getCurrentId()
      self.connection.execute('INSERT INTO backups VALUES("' + currentId + '", "' + projectId + '")')
      if not self.dryRun:
         self.connection.commit()

   '''
   Generates a string id based on the current date: ddmmyyyy
   '''
   def getCurrentId(self):
      today = date.today()
      return today.strftime("%d%m%Y")

   def close(self):
      if self.connection is not None:
         self.connection.close()

   def __connect__(self):
      if self.connection is None:
         self.connection = sqlite3.connect(self.database)
