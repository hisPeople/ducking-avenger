from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import logging

__author__ = 'devonmoss'
FIRST_NAME_THRESHOLD = 90


# class KeyCriteriaError(Exception):
#     def __init__(self, message):
#         self.message = message


# class CompareRules():
#     def __init__(self):
#         self.key_criteria = {}

#     def add_key(self, key, criteria=None):
#         if str(key) in self.key_criteria:
#             raise KeyCriteriaError(
#                 'key: {0} already exists in key_criteria. If you are trying to modify the '
#                 'criteria for a specific key use update_criteria()'.format(key))
#         else:
#             self.key_criteria[key] = criteria

#     def update_criteria(self, key, criteria):
#         self.key_criteria[key] = criteria
def find_match(counselor, members):
    if counselor['member_ID'] == '':
        print 'no member_ID for {0} {1}'.format(counselor['last_name'],counselor['first_name'])
    match = [x for x in members if counselor['member_ID'] == x['member_ID']]
    if len(match):
        print 'found ID match for {0} {1}'.format(counselor['last_name'],counselor['first_name'])
        return {'match_type': 'ID_matched ', 'counselor': counselor, 'match': match[0]}
    else:
        print 'No ID match for {0} {1}'.format(counselor['last_name'],counselor['first_name'])
        match = fuzzy_compare(counselor, members)
        return match

def fuzzy_compare(counselor, members):

    # set the fuzzy search fields for a member
    def set_fields(mem, fields):
        mem.fuzzy_search_fields = fields
        return mem

    def set_threshold(mem, threshold):
        mem.threshold = threshold
        return mem

    log1 = logging.getLogger('Update')

    # collect all members with the same last name as the counselor
    members = [set_fields(x, ['last_name']) for x in members]
    surname_matches = [x for x in members if x == counselor]
    for x in surname_matches:
        x['match'] = False
        print x
    if len(surname_matches):

        # collect address matches from the surname matches - results in Head and Spouse
        surname_matches = [set_fields(x, ['street']) for x in surname_matches]
        household_matches = [x for x in surname_matches if x == counselor]
        # collect phone matches from the surname matches
        surname_matches = [set_fields(x, ['phones']) for x in surname_matches]
        phone_matches = [x for x in surname_matches if x == counselor]
        # collect email matches from the surname matches
        surname_matches = [set_fields(x, ['emails']) for x in surname_matches]
        email_matches = [x for x in surname_matches if x == counselor]

        surname_matches = [set_fields(x, ['first_name']) for x in surname_matches]
        if (len(household_matches) or len(phone_matches) or len(email_matches)):
            # check for exact first name match among household members - confirms an exact counselor match
            match = [x for x in surname_matches if x == counselor and x['match']]
            if len(match):

                return {'match_type': 'matched ', 'counselor': counselor, 'match': match[0]}
            else:
                # find the best first name match in the identified household
                first_names = [x['first_name'] for x in surname_matches if x['match']]
                best_first_name_matches = process.extract(counselor['first_name'], first_names)
                # print 'possible: {0} - {1}'.format(counselor['first_name'], best_first_name_matches)
                if len(best_first_name_matches) and best_first_name_matches[0][1] > 80:
                    best_name_match = best_first_name_matches[0]
                    best_match = [x for x in surname_matches if x['first_name'] == best_name_match[0]]
                    if len(best_match):
                        return {'match_type': 'probable', 'counselor': counselor, 'match': best_match[0]}

        else: # find the best first name match with only surname matching
            first_names = [x['first_name'] for x in surname_matches]
            best_first_name_matches = process.extract(counselor['first_name'], first_names)
            best_name_match = best_first_name_matches[0]
            best_match = [x for x in surname_matches if x['first_name'] == best_name_match[0]]
            # print 'possible: {0} - {1}'.format(counselor['first_name'], best_first_name_matches)
            if len(best_first_name_matches) and best_first_name_matches[0][1] > 80:
#                if len(best_match):
                    return {'match_type': 'possible', 'counselor': counselor, 'match': best_match[0]}
            else:
                members = [set_fields(x, ['street']) for x in members]
                street_matches = [x for x in members if x == counselor]
                different_last_name = [x for x in street_matches if x['last_name'] != counselor['last_name']]
                if len(different_last_name):
                    return {'match_type': 'moved   ', 'counselor': counselor, 'match': street_matches[0]}

        return {'match_type': 'unknown ', 'counselor': counselor, 'match': best_first_name_matches[0]}

    else: # if no surname matches we will change strategy and attempt to prove the counselor doesn't live there anymore.
        members = [set_fields(x, ['street']) for x in members]
        street_matches = [x for x in members if x == counselor]
        different_last_name = [x for x in street_matches if x['last_name'] != counselor['last_name']]
        if len(different_last_name):
            return {'match_type': 'moved   ', 'counselor': counselor, 'match': street_matches[0]}

    return {'match_type': 'unknown ', 'counselor': counselor, 'match': counselor}