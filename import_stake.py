import cProfile

__author__ = 'devonmoss'

from datetime import datetime
import requests
from getpass import getpass
import json
import handle_member_json

username = raw_input('\nEnter Username: ')
print 'To protect privacy, your password not be visible on screen'
password = getpass('Enter Password: ')

auth = {'username': username, 'password': password}
p = requests.post('https://signin.lds.org/login.html', auth)
if 'Sign in' in p.content:
    print 'Authentication Failed. Username and password do not match'
    exit(1)
else:
    cookies = p.cookies
current_user_units = requests.get('https://lds.org/directory/services/ludrs/unit/current-user-units/', cookies=cookies).json()[0]
stake = current_user_units['stakeName']

print '\nDownloading members of {0}\n'.format(stake)

all_names = []

wards = current_user_units['wards']
for ward in wards:
    print '{0}\n'.format(ward['wardName'])
    ward_unit_no = ward['wardUnitNo']
    ward_dir_request_url = 'https://www.lds.org/mobiledirectory/services/v2/ldstools/member-detaillist-with-callings/{0}?lang=eng'.format(ward_unit_no)
    ward_dir = requests.get(ward_dir_request_url, cookies=cookies).json()

    households = ward_dir['households']
    for h in households:    # Can I remove children - Only save H.o.House, Spouse?
        h['ward'] = ward['wardName']
        all_names.append(h)
                
with open('{0}-{1}.json'.format(stake,str(datetime.today()).split()[0]), 'wb') as f:
    f.write(json.dumps(all_names))
    
print 'Data upload completed - Thank You'
print '*** User logged out ***'
# logout = requests.get('https://www.lds.org/signinout/?lang=eng&signmeout', cookies=cookies)

# end of file