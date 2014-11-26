from fuzzy_dict import FuzzyDict
import utils


def make_fuzzy_comparable_member_list(all_households):
    """Format json parsed list of members as a list which can be fuzzy compared and return it.

    """

    heads_and_spouses = []
    for house in all_households:
        for m in ['headOfHouse', 'spouse']:
            person = house[m] if m in house else None
            if person:
                member = FuzzyDict({
                    'first_name': person['preferredName'].split(',')[1].strip(),
                    'last_name': person['surname'], 'street': house['desc1'] if 'desc1' in house else '',
                    'phone': utils.normalize_phone_number(person['phone']) if 'phone' in person else utils.normalize_phone_number(
                        house['phone']) if 'phone' in house else '',
                    'email': person['email'] if 'email' in person else house['email'] if 'email' in house else ''
                })
                heads_and_spouses.append(member)

    return heads_and_spouses