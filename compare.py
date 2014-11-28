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

    # set the fuzzy search fields for a member
    def set_fields(mem, fields):
        mem.fuzzy_search_fields = fields
        return mem

    def set_threshold(mem, threshold):
        mem.threshold = threshold
        return mem

    members = [set_fields(x, ['last_name', 'first_name', 'street']) for x in members]
    matches = [x for x in members if x == counselor]
    if len(matches):
        return {'match_type': 'exact', 'counselor': counselor, 'match': matches[0]}

    else:
        # return any with same lastname and address:
        members = [set_fields(x, ['last_name', 'street']) for x in members]
        name_street_matches = [x for x in members if x == counselor]

        # get list of first names form the returned name_street_matches
        first_names = [x['first_name'] for x in name_street_matches]

        # return best first name matches
        best_first_name_matches = process.extract(counselor['first_name'], first_names)
        if len(best_first_name_matches) and best_first_name_matches[0][1] > 85:
            best_name_match = best_first_name_matches[0]
            best_match = [x for x in name_street_matches if x['first_name'] == best_name_match[0]]
            if len(best_match):
                return {'match_type': 'first_name_widen', 'counselor': counselor, 'match': best_match[0]}


        # if that didn't find one we will change strategy and attempt to prove the counselor doesn't live there anymore.
        members = [set_fields(x, ['street']) for x in members]
        street_matches = [x for x in members if x == counselor]
        different_last_name = [x for x in street_matches if x['last_name'] != counselor['last_name']]

        if len(different_last_name):
            return {'match_type': 'positive_mismatch', 'counselor': counselor, 'match': None}


    return {'match_type': None, 'counselor': counselor, 'match': None}