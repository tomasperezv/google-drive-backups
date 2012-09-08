google-drive-backups
=============
Python application to store backups in the Google Drive storage service.

Multiple jobs can be configured. An example of the configuration(config/config.json):

	"jobs": [
		{
			"id": "project-id",
			"folder": "jobs",
			"script": "script-that-generates-the-backup.sh",
			"filename": "output.txt",
			"remote_folder": "google-drive-id-of-the-remote-folder"
		}
	]

It keeps track of the backups in a local sqlite database.

TODO:
	- Replace the sqlite database for direct queries against the Google Drive API.

Author
----------
Tomas Perez - tom@0x101.com

http://www.tomasperez.com

License
-----------
Public Domain.

No warranty expressed or implied. Use at your own risk.
