import csv
from fuzzy_dict import FuzzyDict
import utils


def load_counselors(counselors_file_path, stake):
    """Parse counselors file for counselors in specified stake and return them in a list of parsed csv file rows.
    """
    print '\nloading ',counselors_file_path, ' for ', stake, ' stake'
    with open(counselors_file_path, 'rb') as f:
        # dialect = csv.Sniffer().sniff(f.read(1024))
        # f.seek(0)
        # reader = csv.reader(f, dialect)
        reader = csv.reader(f, delimiter='\t')
        if stake == 'all':
            viewable_members = [x for x in reader]  # Need to remove header row.
        else:
            viewable_members = [x for x in reader if (str(x[13]) == str(stake))]

    return viewable_members

def load_dist_ypt(ypt_file_path):
    """Load district members file from council with Youth Protection Training Dates """
    scouters = 0

    with open(ypt_file_path, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        dist_members = [x for x in reader]

        for row in reader:
            member_ID = row[0]
            stake_name = c[5],
            dist_position = c[45],

            # This is to skip the header row
            if ( scouters == 0 ):
                if ( member_ID != 'Person ID' ):
                    dist_members.append(row)
                    scouters += 1
                    print member_ID

            # if this line is a new person, add their record
            elif ( member_ID != dist_members[scouters-1][0] ):
                dist_members.append(row)
                scouters += 1
                print member_ID

            # This person is already recorded, but only shows district data
            # Replace the record, retaining only the district position name
            elif len(dist_members[scouters-1][5]):
                dist_pos = dist_members[scouters-1][45]
                g = dist_members.pop(scouters-1)
                dist_members.append(row)
                dist_members[scouters-1][45] = dist_pos

            # This person has a record in place with only unit position data
            # If this line read is a district position, add it to their record
            elif (len(dist_position) and (len(dist_members[scouters-1][45]) == 0)):
                dist_members[scouters-1][45] = dist_position

    return dist_members


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
            'last_name':  c[0],
            'first_name': c[1],
            'street':     c[2],
            'city':       c[3],  # state c[4], and Postal Code c[5] not used
            'phones': {
                'phone2': utils.normalize_phone_number(c[6]),
                'phone1': utils.normalize_phone_number(c[7])
            },
            'emails': {
                'email1': c[8],
                'email2': c[9]
            },
            'Y01':        c[10], # Expired date c[11] not used
            'Y02':        c[12],
            'stake':      c[13],
            'member_ID':  c[14], # Active and Show Address checkboxes c[15,16] not used
            'note':       c[17]
        })
        # print counselor_dict
        fuzzy_list.append(counselor_dict)

    return fuzzy_list

def make_fuzzy_comparable_district_list(scouters):

    fuzzy_d_list = []

    for c in scouters:
        if c[0] == 'Person ID  ':
            print 'skipping header row'
        elif len(fuzzy_d_list) and c[0] == fuzzy_d_list[len(fuzzy_d_list)-1]['member_ID']:
            print 'skipping duplicate {0} {1}'.format(c[14],c[16])
        else:
            print 'adding scouter {0} {1}'.format(c[14],c[16])
            scouter_dict = FuzzyDict({
                'member_ID':     c[0],
                'first_name':    c[14],
                'middle_name':   c[15],
                'last_name':     c[16],
#                'full_name':     c[14] c[15] c[16],
                'age':           c[21],
                'gender':        c[24],
                'street':        c[29],
                'phones': {
                    'phone1': utils.normalize_phone_number(c[53]),
                    'phone2': ''
                },
                'emails': {
                    'email1':    c[87],
                    'email2':    c[88]
                },
                'stake': utils.stake_ID(c[4]) if len(c[4]) else utils.stake_ID(c[43]), 
                'ward':          c[11],
                'unit_number':   c[7],
                'unit_pos':      c[38],
                'dist_unit':     c[43],
                'dist_pos':      c[45],
                'Y01':           c[57],
                'Y02':           c[58],
                'award_name':    c[94],
                'award_date':    c[95],
                'MBC_code':      c[104],
                'MBC_unit_only': c[108]
            })
            fuzzy_d_list.append(scouter_dict)
    return fuzzy_d_list
