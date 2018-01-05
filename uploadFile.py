import os
from os.path import basename

import apiclient
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def uploadOnlyDirectory(dirName, drive_service, parentsID=None):
    file_metadata = {
    'name': dirName,
    'mimeType': 'application/vnd.google-apps.folder'
    }

    if not(parentsID is None):
        file_metadata['parents'] = [parentsID]

    folder = drive_service.files().create(body=file_metadata,fields='id, name').execute()
    print('Folder %s: %s' % (folder.get('name'), folder.get('id')))
    return folder.get('id')

def uploadFile(filePath, fileName, drive_service, parentsID=None):
    # FILENAME = 'test/'
    MIMETYPE = 'application/vnd.google-apps.unknown'

    media_body = apiclient.http.MediaFileUpload(
        filePath,
        resumable=True
    )
    # The body contains the metadata for the file.
    body = {
        'name': fileName
    }
    if not(parentsID is None):
        body['parents'] = [parentsID]
    # Perform the request and print the result.
    new_file = drive_service.files().create(body=body, media_body=media_body,fields='id, name').execute()
    print('File %s: %s' % (new_file.get('name'), new_file.get('id')))
    # print('File ID: %s' % new_file.get('id'))

def uploadFileAndDirectory(dirName, path, drive_service, folderID=None):
    # path = '/Users/administrator/Desktop/python-quickstart-master/test'
    rootID = uploadOnlyDirectory(dirName, drive_service, folderID)

    for f in os.listdir(path):
        path_file = path + '/' + f
        if os.path.isdir(path_file):
            uploadFileAndDirectory(f, path_file, drive_service, rootID)
        if os.path.isfile(path_file) and os.path.getsize(path_file) > 0 and not f.startswith('.'):
            print f
                # print(basename(f))
            uploadFile(path_file, f, drive_service, rootID)

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = apiclient.discovery.build('drive', 'v3', http=http)

    path = '/Users/administrator/Desktop/python-quickstart-master/test'
    uploadFileAndDirectory('test', path, drive_service)
    #uploadOnlyDirectory('app', drive_service)
if __name__ == '__main__':
    main()
