__author__ = 'devonmoss'

import requests
import csv
import json

# auth = {'username': '***', 'password': '***'}
# p = requests.post('https://signin.lds.org/login.html', auth)
# cookies = p.cookies
#
# current_user_units = requests.get('https://lds.org/directory/services/ludrs/unit/current-user-units/', cookies=cookies).json()[0]
# stake = current_user_units['stakeName']
#
# print 'listing memebers for {0}\n'.format(stake)
#
# all_names = []
#
# wards = current_user_units['wards']
# for ward in wards:
#     print '\n{0}\n'.format(ward['wardName'])
#     ward_unit_no = ward['wardUnitNo']
#     ward_dir_reqeust_url = 'https://www.lds.org/mobiledirectory/services/v2/ldstools/member-detaillist-with-callings/{0}?lang=eng'.format(ward_unit_no)
#     ward_dir = requests.get(ward_dir_reqeust_url, cookies=cookies).json()
#
#     with open('{0}.json'.format(ward['wardName']), 'wb') as f:
#         f.write(json.dumps(ward_dir))
    # for house in ward_dir:
    #     print house['headOfHouse']['preferredName']
        # all_names.append(house['headOfHouse']['preferredName'])

#

stake_members = []
with open('path/to/CounselorList141108.csv', 'rb') as f:
    dialect = csv.Sniffer().sniff(f.read(1024))
    f.seek(0)
    reader = csv.reader(f, dialect)
    for row in reader:
        stake = row[13]
        last_name = row[0]
        first_name = row[1]
        street_address = row[2]
        work_phone = row[6]
        home_phone = row[7]
        email1 = row[8]
        email2 = row[9]

        if 'Pleasant Grove East' in stake:
            stake_members.append(row)
            print 'added work_phone: {0}'.format(work_phone)


        # if gen_prefered_name in all_names:
        #     print '{0} was found'.format(gen_prefered_name)

# if 'Pleasant Grove East' in row[13]:
#     print row[0]

# for row in reader:
#     k, v = row
#     print k
#     print v
#     if 'Pleasant Grove East' in row['Group']:
#         print row



member_file_list = [
    'Battle Creek  1st Ward.json',
    'Battle Creek  2nd Ward.json',
    'Battle Creek  3rd Ward.json',
    'Battle Creek  4th Ward.json',
    'Battle Creek  5th Ward.json',
    'Battle Creek  6th Ward.json',
    'Battle Creek  7th Ward.json',
    'Battle Creek  8th Ward.json',
    'Battle Creek  9th Ward.json',
    'Battle Creek 10th Ward.json'
]


def read_in_files():
    all_households = []
    for filename in member_file_list:
        # print 'reading file {0}'.format(filename)
        with open(filename, 'r') as f:
            data = json.load(f)
            households = data['households']
            for h in households:
                all_households.append(h)
        # print 'done reading file {0}'.format(filename)

    # households_with_name = [x for x in all_households if 'Adams' in x['householdName']]
    #
    # if len(households_with_name):
    #     for h in households_with_name:
    #         print h
    print 'all_households: {0}'.format(len(all_households))
    print 'stake_members: {0}'.format(len(stake_members))
    for row in stake_members:
        has_phone = [x for x in all_households if 'phone' in x]
        phone_matches_work = [x for x in has_phone if row[6] and row == x['phone']]
        phone_matches_home = [x for x in has_phone if row[7] == x['phone']]

    if len(phone_matches_work):
        print 'work phone matches: {0}'.format(len(phone_matches_work))
    if len(phone_matches_home):
        print 'home phone matches: {0}'.format(len(phone_matches_home))
        # for m in phone_matches:
        #     # print 'exact match for phone number: {0}'.format(m['phone'])
        #     pass
read_in_files()


"""
    logic for uniquely identifying people
    -relevant fields are last name, first name, phone, address, email

    ** option 1 **
        for each name in counselor list:
            get phone
            search mem directory for exact household phone match
                if match found:
                    validate by comparing accuracy to other fields
                else:
                    expand search to all records with same last name
                    for each same name household:
                        look for listed phone numbers of any household member (presumably to get cell phone numbers)
                            if match found:
                                validate by comparing accuracy to other fields
                            else:
                                expand fallback search

    ** option 2 **
        for each name in counselor list:
            get phone, email, address, first name, last name
            search mem directory for (exact match to (any field) and (last name))

    fallback option:
        take all relevant data: name, phone, address, email and do a fuzzy search to compare it all
"""