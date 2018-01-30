from __future__ import print_function
import httplib2
import os
import pprint
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import apiclient.discovery
import apiclient.http

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json

#SCOPES = 'https://www.googleapis.com/auth/drive'
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
MIMETYPE = 'text/plain'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    print("getting credentials...")

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            print('flags with things.')
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            print('flags is none')
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def UploadFile(filename,folder_id):
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    #print("uploading init done.")
    if False:
        results = service.files().list(
            pageSize=10,fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))
    else:
        print("uploading file : ",filename," to folder : ",folder_id)
        if False:
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            media = apiclient.http.MediaFileUpload(filename,
                            mimetype=MIMETYPE,
                            resumable=True)
            file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields=folder_id).execute()
            print ('File ID: ',file.get('id'))
        else:
            media_body = apiclient.http.MediaFileUpload(
                filename,
                mimetype = MIMETYPE,
                resumable = True
            )
            # The body contains the metadata for the file.
            body = {
              "name": filename,
              "parents": [folder_id],
            }

            # Perform the request and print the result.
            new_file = service.files().create(body=body, media_body=media_body).execute()
            print("upload finished!")
            pprint.pprint(new_file)
