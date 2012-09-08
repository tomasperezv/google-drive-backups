#!/usr/bin/python

import json
from backup.backup_job import BackupJob, BackupJobException
from backup.database_backup import DataBaseBackup
from backup.google_drive import GoogleDriveStorage

# Load the config
rawConfig = open('./config/config.json', 'r').read()
config = json.loads(rawConfig)

# Initialize the backup manager
databaseBackup = DataBaseBackup(config['database'], config['dry_run'])

for project in config['jobs']:
   if databaseBackup.pending(project['id']):
      print 'Generating backup for ' + project['id'] +': ' + databaseBackup.getCurrentId()

      # The backup job class will execute the external scrip that builds the
      # backup file.
      backupJob = BackupJob(project['folder'], project['script'], project['filename'])
      try:
         filename = backupJob.run()
         # Send the backup to the google drive service
         googleDrive = GoogleDriveStorage(config['google_drive']['client_id'], config['google_drive']['client_secret'], config['google_drive']['scope'])
         if googleDrive.send(databaseBackup.getCurrentId(), filename, project['remote_folder']):
            databaseBackup.add(project['id'])

      except BackupJobException:
         print 'Something went wrong generating the backup for ' + project['id']

databaseBackup.close()
