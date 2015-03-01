''' Output Accounts + Containers to txt '''

import argparse
import sys

import httplib2

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools

def main(argv):
   
    # Define variable constants for the application
    CLIENT_SECRETS = 'client_secrets.json'
    SCOPE = ['https://www.googleapis.com/auth/tagmanager.readonly']

    # Parse command-line arguments
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flags = parser.parse_args()
    
    # Set up a Flow object tobe used if we need to authenticate
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope=SCOPE,
        message=tools.message_if_missing(CLIENT_SECRETS))
    
    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid, run through the native client
    # flow. The Storage object will ensure that if successful, the good
    # credentials will be written back to a file.
    storage = file.Storage('tagmanager.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())
    
    # Build the service object
    service = build('tagmanager', 'v1', http=http)
    
    # Get all accounts the user has access to
    accounts = service.accounts().list().execute()

    # If the user has access to accounts, open accounts.txt and
    # write the account and container names the user can access
    if len(accounts):
        with open('accounts.txt', 'w') as f:
            for a in accounts['accounts']:
                f.write('Account: ' + 
                        unicode(a['name']).encode('utf-8') + 
                        '\n')
                # Get all the containers under each account
                containers = service.accounts().containers().list(
                    accountId=a['accountId']).execute()
                if len(containers):
                    for c in containers['containers']:
                        f.write('Container: ' + 
                                unicode(c['name']).encode('utf-8') + 
                                '\n')
if __name__ == '__main__':
  main(sys.argv)
