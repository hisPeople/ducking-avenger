from fuzzywuzzy import process
from fuzzywuzzy import fuzz

__author__ = 'devonmoss'
FIRST_NAME_THRESHOLD = 90


class KeyCriteriaError(Exception):
    def __init__(self, message):
        self.message = message


class CompareRules():
    def __init__(self):
        self.key_criteria = {}

    def add_key(self, key, criteria=None):
        if str(key) in self.key_criteria:
            raise KeyCriteriaError(
                'key: {0} already exists in key_criteria. If you are trying to modify the '
                'criteria for a specific key use update_criteria()'.format(key))
        else:
            self.key_criteria[key] = criteria

    def update_criteria(self, key, criteria):
        self.key_criteria[key] = criteria


def fuzzy_compare(counselor, members):

    # exact_matches = []
    # non_exact_matches = []
    # # check for exact matches to phone
    # same_phone = [x for x in members if x['phone'] and x['phone'] in counselor['phones'].values()]
    #
    # # check for exact matches to email
    # same_email = [x for x in members if x['email'] and x['email'] in counselor['emails'].values()]
    #
    # # check for exact matches to address
    # same_address = [x for x in members if x['street'] and x['street'] in counselor['street']]
    #
    # # check for exact matches to Last Name
    # same_last = [x for x in members if x['last_name'] == counselor['last_name']]
    #
    # # check for first name match
    # same_first_and_last = [x for x in same_last if fuzz.ratio(x['first_name'], counselor['first_name']) > FIRST_NAME_THRESHOLD]

    matches = [x for x in members if x == counselor]

    if len(matches):
        for match in matches:
            print 'match found:'
            print 'last name: {0} = {1}'.format(match['last_name'], counselor['last_name'])
            print 'first name: {0} = {1}'.format(match['first_name'], counselor['first_name'])
            print 'street: {0} = {1}'.format(match['street'], counselor['street'])
            print 'phone: {0} = {1} or {2}'.format(match['phone'], counselor['phones']['work'], counselor['phones']['home'])
            print 'email: {0} = {1} or {2}'.format(match['email'], counselor['emails']['primary'], counselor['emails']['secondary'])
            print
    else:
        print 'no match found for {0} {1}'.format(counselor['first_name'], counselor['last_name'])

    return len(matches)
    # intersect = set(same_phone).intersection(set(same_email)).intersection(set(same_last))
    # if len(same_phone):
    #     phone_intersect = [x for x in same_phone if x in same_last]
    #
    # if len(same_email):
    #     email_intersect = [x for x in same_email if x in same_last]
    #
    # if len(same_address):
    #     address_intersect = [x for x in same_address if x in same_last]
    #
    #
    #
    # exact_match = len(same_phone) + len(same_email) + len(same_last) > 1
    #
    #
    # if exact_match:
    #     # validate with the rest of the fields
    #     exact_matches.append(counselor)
    #     # print 'Exact match found for {0} {1}'.format(counselor['first_name'], counselor['last_name'])
    # else:
    #     # print 'No exact match found for {0} {1}. Fuzzy search results:'.format(counselor['first_name'], counselor['last_name'])
    #     # fuzzy email
    #     non_exact_matches.append(counselor)
    #     # email_choices = [x['email'] for x in members]
    #     # for email in counselor['emails'].values():
    #     #     if email:
    #     #         print 'top email matches for {0}'.format(email)
    #     #         closest_matches = process.extract(email, email_choices)
    #     #         for c in closest_matches:
    #     #             print '{0} -- confidence: {1}'.format(c[0], c[1])
    #     #
    #     # #fuzzy address
    #     # address_choices = [x['street'] for x in members]
    #     # street = counselor['street']
    #     # if street:
    #     #     print 'top street matches for {0}'.format(street)
    #     #     closest_matches = process.extract(street, address_choices)
    #     #     for c in closest_matches:
    #     #         print '{0} -- confidence: {1}'.format(c[0], c[1])