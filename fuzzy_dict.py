from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def _is_fuzzy_match(s1, s2, threshold=90):
    if isinstance(s2, dict):
        best_match = process.extractOne(s1, s2.values(), score_cutoff=90)
        return True if best_match else False
    return fuzz.ratio(s1, s2) > threshold


class FuzzyDict(dict):
    _key_names = ['first_name', 'last_name', 'street', 'phone', 'email']
    def __hash__(self):
        # todo -- implement hashcode
        total_hash_val = 0
        for k in self.keys():
            total_hash_val = hash(self[k])
        return total_hash_val

    def __eq__(self, other):
        if isinstance(other, FuzzyDict):
            # todo -- set equality based on fuzzy compare

            first_name_matches = _is_fuzzy_match(self['first_name'], other['first_name'])
            last_name_matches = _is_fuzzy_match(self['last_name'], other['last_name'])
            street_matches = _is_fuzzy_match(self['street'], other['street'])

            # handle multiple phones todo -- abstract
            if 'phones' in other.keys():
                phone_matches = _is_fuzzy_match(self['phone'], other['phones'])
            elif 'phones' in self.keys():
                phone_matches = _is_fuzzy_match(other['phone'], self['phones'])
            else:
                phone_matches = _is_fuzzy_match(self['phone'], other['phone'])

            # handle multiple emails todo -- abstract
            if 'emails' in other.keys():
                email_matches = _is_fuzzy_match(self['email'], other['emails'])
            elif 'emails' in self.keys():
                email_matches = _is_fuzzy_match(other['email'], self['emails'])
            else:
                email_matches = _is_fuzzy_match(self['email'], other['email'])

            if first_name_matches and last_name_matches and street_matches:
                return True

            return False

            # match_ratio_sum = 0
            # for k in self.keys():
            #     match_ratio_sum = match_ratio_sum + fuzz.ratio(self[k], other[k])
            # composite_ratio = match_ratio_sum/len(self.keys())
            # return composite_ratio > 90
        return NotImplemented

