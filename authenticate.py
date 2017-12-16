import configparser

from dropbox import Dropbox, DropboxOAuth2FlowNoRedirect

import config


def add_token(config_file):
    key = config_file['APP_CREDS']['app_key']
    secret_key = config_file['APP_CREDS']['secret_app_key']
    auth_flow = DropboxOAuth2FlowNoRedirect(key, secret_key)
    authorize_url = auth_flow.start()
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first).')
    print('3. Copy the authorization code.')
    auth_code = input('Enter the authorization code here: ').strip()
    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        print('Error: ', e)
    account_info = Dropbox(oauth_result.access_token).users_get_current_account()
    config_file['USER_CREDENTIALS'] = {
        'user_name': account_info.name.display_name,
        'email': account_info.email,
        'account_id': account_info.account_id,
        'oauth_key': oauth_result.access_token
    }
    with open(config.CREDS_FILE, 'w') as f:
        config_file.write(f)
    return oauth_result.access_token


def get_user_creds():
    config.verify_config_file()
    config_file = configparser.ConfigParser()
    config_file.read(config.CREDS_FILE)
    if 'USER_CREDENTIALS' not in config_file.sections():
        return add_token(config_file)
    return config_file['USER_CREDENTIALS']['oauth_key']
