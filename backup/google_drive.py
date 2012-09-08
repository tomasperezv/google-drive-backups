import httplib2

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

'''
@class GoogleDriveStorage
@author tom@0x101.com

Send files to the google drive storage service.
'''

class GoogleDriveStorage:


   # Parameters related with the oAuth2 validation
   clientId = None
   secret = None
   scope = None
   url = 'urn:ietf:wg:oauth:2.0:oob'

   def __init__(self, clientId, secret, scope):
      self.clientId = clientId
      self.secret = secret
      self.scope = scope

   def __getCredentials__(self):
      flow = OAuth2WebServerFlow(self.clientId, self.secret, self.scope)
      authorize_url = flow.step1_get_authorize_url(self.url)

      print 'Go to the following link in your browser: ' + authorize_url
      code = raw_input('Enter verification code: ').strip()

      return flow.step2_exchange(code)

   def send(self, id, filename, folderId = None):
      credentials = self.__getCredentials__()

      http = httplib2.Http()
      http = credentials.authorize(http)

      drive_service = build('drive', 'v2', http=http)

      # Insert a file
      media_body = MediaFileUpload(filename, mimetype='text/plain', resumable=True)
      body = {
         'title': id,
         'description': 'Backup ' + id,
         'parents': [{"id": folderId}]
      }

      file = drive_service.files().insert(body=body, media_body=media_body).execute()

      return file is not None
