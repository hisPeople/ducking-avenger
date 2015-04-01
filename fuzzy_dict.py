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
    ratio_1 = fuzz.token_set_ratio(s1, s2)
    ratio_2 = fuzz.token_set_ratio(s2, s1)
    best = ratio_1 if ratio_1 > ratio_2 else ratio_2
    return best > threshold


class FuzzyDict(dict):
    _key_names = ['first_name', 'last_name', 'street', 'phones', 'emails']

    fuzzy_search_fields = None
    threshold = 90

    def __hash__(self):
        # todo -- implement hashcode
        total_hash_val = 0
        for k in self.keys():
            total_hash_val = hash(self[k])
        return total_hash_val

    def __eq__(other, self):
        if isinstance(other, FuzzyDict):
            for field in other.fuzzy_search_fields:
                if field == 'street':
                    if _is_fuzzy_token_set_match(self[field], other[field]):

                        """ Add code here to extract numeric portions of addresses and compare for exact match-
                            If the token match is close, and the numbers are exact, the addresses match.
                        """
                        other['match'] = True
                        return True

                elif field == 'phones':
                    if 'phone1' in self['phones']:
                        if ((self['phones']['phone1'] == other['phones']['phone1']) or
                            (self['phones']['phone1'] == other['phones']['phone2'])):
                            other['match'] = True
                            return True
                    if 'phone2' in self['phones']:
                        if ((self['phones']['phone2'] == other['phones']['phone1']) or
                            (self['phones']['phone2'] == other['phones']['phone2'])):
                            other['match'] = True
                            return True
                    # if 'phone1' in self['phones']:
                    #     if ((self.phones['phone1'] == other.phones['phone1']) or
                    #         (self.phones['phone1'] == other.phones['phone2'])):
                    #         return True
                    # if 'phone2' in self['phones']:
                    #     if ((self.phones['phone2'] == other.phones['phone1']) or
                    #         (self.phones['phone2'] == other.phones['phone2'])):
                    #         return True

                elif field == 'emails':
                    if   len(self['emails']['email1']):
                        if ((self['emails']['email1'] == other['emails']['email1']) or
                            (self['emails']['email1'] == other['emails']['email2'])):
                            other['match'] = True
                            return True
                    if   len(self['emails']['email2']):
                        if ((self['emails']['email2'] == other['emails']['email1']) or
                            (self['emails']['email2'] == other['emails']['email2'])):
                            other['match'] = True
                            return True
                        
                else:
                    if _is_fuzzy_match(self[field], other[field], threshold=self.threshold):
                        return True

            return False

        return NotImplemented

