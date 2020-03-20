from config.secrets import auth_token

api_url = 'https://api.tempo.io/core/3/'
api_url_worklogs = api_url + 'worklogs'

auth_header = {'Authorization': 'Bearer ' + auth_token}
