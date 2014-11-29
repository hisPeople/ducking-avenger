from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def _is_fuzzy_match(s1, s2, threshold=90):
    if isinstance(s2, dict):
        best_match = process.extractOne(s1, s2.values(), score_cutoff=threshold)
        return True if best_match else False
    #for debugging TODO: REMOVE
    ratio = fuzz.ratio(s1, s2)
    # print '{0} ==> {1} :: {2}'.format(s1, s2, ratio)
    return fuzz.ratio(s1, s2) > threshold


def _is_fuzzy_token_set_match(s1, s2, threshold=90):
    #for debugging TODO: REMOVE
    # ratio_1 = fuzz.token_set_ratio(s1, s2)
    # ratio_2 = fuzz.token_set_ratio(s2, s1)
    # best = ratio_1 if ratio_1 > ratio_2 else ratio_2
    return fuzz.token_set_ratio(s1, s2) > threshold


class FuzzyDict(dict):
    _key_names = ['first_name', 'last_name', 'street', 'phone', 'email']

    fuzzy_search_fields = None
    threshold = 90

    def __hash__(self):
        # todo -- implement hashcode
        total_hash_val = 0
        for k in self.keys():
            total_hash_val = hash(self[k])
        return total_hash_val

    def __eq__(self, other):
        if isinstance(other, FuzzyDict):
            for field in self.fuzzy_search_fields:
                if field == 'street':
                    if not _is_fuzzy_token_set_match(self[field], other[field]):
                        return False
                else:
                    if not _is_fuzzy_match(self[field], other[field], threshold=self.threshold):
                        return False

            return True

            # first_name_matches = _is_fuzzy_match(self['first_name'], other['first_name'])
            # last_name_matches = _is_fuzzy_match(self['last_name'], other['last_name'])
            # street_matches = _is_fuzzy_match(self['street'], other['street'])

            # # handle multiple phones todo -- abstract
            # if 'phones' in other.keys():
            #     phone_matches = _is_fuzzy_match(self['phone'], other['phones'])
            # elif 'phones' in self.keys():
            #     phone_matches = _is_fuzzy_match(other['phone'], self['phones'])
            # else:
            #     phone_matches = _is_fuzzy_match(self['phone'], other['phone'])
            #
            # # handle multiple emails todo -- abstract
            # if 'emails' in other.keys():
            #     email_matches = _is_fuzzy_match(self['email'], other['emails'])
            # elif 'emails' in self.keys():
            #     email_matches = _is_fuzzy_match(other['email'], self['emails'])
            # else:
            #     email_matches = _is_fuzzy_match(self['email'], other['email'])

            # if first_name_matches and last_name_matches and street_matches:
            #     return True
            #
            # return False

            # match_ratio_sum = 0
            # for k in self.keys():
            #     match_ratio_sum = match_ratio_sum + fuzz.ratio(self[k], other[k])
            # composite_ratio = match_ratio_sum/len(self.keys())
            # return composite_ratio > 90
        return NotImplemented

