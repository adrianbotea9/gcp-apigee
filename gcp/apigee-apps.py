import google.auth
from google.auth.transport import requests as auth_transport
from google.oauth2 import service_account
import requests
import json
import argparse
from typing import List, Dict, Optional

class ApigeeClient:
    def __init__(self, organization: str, credentials_path: str):
        '''
        Init Apigee client with organization ID and path to credentials json
        '''
        self.organization = organization
        self.url = f"https://apigee.googleapis.com/v1/organizations/{organization}"
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
        #create authentication request object for when the token expires and needs to be renewed
        self.auth_request = auth_transport.Request()


    def _get_headers(self) -> Dict[str, str]:
        '''
        Get authenticated headers for api requeests
        '''
        if not self.credentials.valid:
            #using the class member fr token refresh
            self.credentials.refresh(self.auth_request)
        return {
            'Authorization': f'Bearer {self.credentials.token}',
            'Content-Type': 'application/json'
        }
      
        
    def get_app_details(self, app_id: str) -> Dict:
        '''
        Because GET url/apps only returnS app id this method will return the rest of the app details
        '''
        url = f"{self.url}/apps/{app_id}"
        response = requests.get(url, headers=self._get_headers())
        #check if request was succesful
        response.raise_for_status()
        return response.json()


    def list_apps(self) -> List[Dict]:
        '''
        List all the apps in the given org

        Returns: List of dictionaries containing app ids
        '''
        url = f"{self.url}/apps"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        apps = response.json().get('app', [])
        formatted_apps = []
        for app in apps:
            app_id = app.get('appId')
            try:
                app_details = self.get_app_details(app_id)
        
                formatted_app = {
                    "appId": app_id,
                    "name": app_details.get('name'),
                    "developerId": app_details.get('developerId')
                }
                formatted_apps.append(formatted_app)
            except Exception as e:
                print(f"Error getting details for app {app_id}: {e}")
            
        return {"apps": formatted_apps}
    

    def list_developer_apps(self, dev_mail: str) -> List[Dict]:
        '''
        List all apps belonging to a specific developer

        Args: dev_mail: mail address of the developer

        Returns: List of appID dictionaries for the sprecific developer
        '''

        url = f"{self.url}/developers/{dev_mail}/apps"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json().get('app', [])
    

    def create_app(self, dev_mail: str, app_name: str, callback_url: Optional[str] = None , description: Optional[str] = None) -> Dict:
        '''
        Create a new app for a developer

        Args: 
            dev_mail: mail address of the developer
            app_name: name for the new app
            callback_url: optional callback URL for the new app
            description: optional description for the new app

        Returns: Dictionary containing the new app details
        '''

        url = f"{self.url}/developers/{dev_mail}/apps"

        app_data = {
            "name": app_name,
            "callback_url": callback_url,
            "escription": description
        }
        #remove from the payload if one of the optional args is None 
        app_data = {k: v for k, v in app_data.items() if v is not None}

        response = requests.post(url, headers=self._get_headers(), json=app_data)
        response.raise_for_status()
        return response.json()

def main():
    parser = argparse.ArgumentParser(description='List Apigee apps')
    parser.add_argument('--organization', required=True, help='Org id')
    parser.add_argument('--credentials', required=True, help='Path to SA json')
    parser.add_argument('--action', required=True, choices=['list-all', 'list-developer', 'create'], help='Action to perform')
    parser.add_argument('--dev-mail', help='developer email address')
    parser.add_argument('--app-name', help='App name to be created')
    parser.add_argument('--callback-url', help='Callback url for new app')
    parser.add_argument('--description', help='Description for new app')

    args = parser.parse_args()
    
    client = ApigeeClient(args.organization, args.credentials)

    try:
        if args.action == 'list-all':
            apps = client.list_apps()
            print(json.dumps(apps, indent=2))
        elif args.action == 'list-developer':
            if not args.dev_mail:
                raise ValueError("developer mail required")
            apps = client.list_developer_apps(args.dev_mail)
            print(json.dumps(apps, indent=2))
        elif args.action == 'create':
            if not args.dev_mail or not args.app_name:
                raise ValueError('developer mail and app name required')
            app = client.create_app(args.dev_mail, args.app_name, args.callback_url, args.description)
            print(json.dumps(app, indent=2)) 

    #handle API request errors
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        #check if the error has a response object
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        exit(1)
    #handle other errors
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
