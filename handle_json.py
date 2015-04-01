from fuzzy_dict import FuzzyDict
import utils
import json


def read_in_stake(stake):
    all_households = []
    print '\nloading LDS Tools data for ', stake, ' stake'
    with open(stake, 'r') as f:
        data = json.load(f)
        # print data
        # households = data['households']
        for h in data:
            all_households.append(h)
    return all_households

def make_fuzzy_comparable_member_list(all_households):
    """Format json parsed list of members as a list which can be fuzzy compared and return it. """

    heads_and_spouses = []
    for house in all_households:
        for m in ['headOfHouse', 'spouse']:
            person = house[m] if m in house else None
            if person:
                member = FuzzyDict({
                    'first_name': person['preferredName'].split(',')[1].strip() if ',' in person['preferredName'] else '',
                    'last_name': person['surname'] if 'surname' in house[m] else '', 
                    'full_name': person['fullName'] if 'fullName' in house[m] else 'fail',
                    'street': house['desc1'] if 'desc1' in house else '',
                    'phones': {
                        'phone1': utils.normalize_phone_number(person['phone']) if 'phone' in person else 0,
                        'phone2': utils.normalize_phone_number( house['phone']) if 'phone' in  house else 0
                    },
                    'emails': {
                        'email1' : person['email'] if 'email' in person else '',
                        'email2': house['email'] if 'email' in  house else ''
                    },
                    'ward': house['ward'],
                    'match': False
                })
                # print member
                heads_and_spouses.append(member)

    return heads_and_spouses