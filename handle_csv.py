import csv
from fuzzy_dict import FuzzyDict
import utils


def get_counselors_in_stake(counselors_file_path, stake):
    """Parse counselors file for counselors in specified stake and return them in a list of parsed csv file rows.

    Args:
        counselors_file_path (str) -- Path to counselors csv file
        stake (str) -- Name of current user's Stake

    Returns:
        list. Counselors in the current users stake
    """
    with open(counselors_file_path, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        viewable_members = [x for x in reader if str(x[13]) == str(stake)]

    return viewable_members


def make_fuzzy_comparable_counselor_list(counselors):
    """Format list of parsed csv rows of counselors as list which can be fuzzy compared and return it.

    Args:
        counselors (list) -- List of parsed csv rows

    Returns:
        list. Formatted list of dictionaries containing relevant fields for fuzzy comparison::

        [
            {
                last_name: 'Smith',
                first_name: 'Jonathan',
                street: '1234 Meadow Ln',
                emails: {
                    primary: 'johnsmith@gmail.com',
                    secondary: 'jsmitty345@hotmail.com'
                },
                phone: {
                    work: '1234567890',
                    home: '1232323242'
                }
            }
        ]
    """
    fuzzy_list = []
    for c in counselors:
        counselor_dict = FuzzyDict({
            'last_name': c[0],
            'first_name': c[1],
            'street': c[2],
            'emails': {
                'primary': c[8],
                'secondary': c[9]
            },
            'phones': {
                'work': utils.normalize_phone_number(c[6]),
                'home': utils.normalize_phone_number(c[7])
            }
        })
        fuzzy_list.append(counselor_dict)

    return fuzzy_list