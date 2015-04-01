__author__ = 'bert'

import sys
import requests
import csv
import json
import handle_json
import handle_csv
import compare
import logging
from datetime import datetime

# Set up logging file to receive Update record

stake_list = [
    'Garden',
    'Grove Creek',
    'Lindon',
    'Lindon Central',
    'Lindon West',
    'Mount Mahogany',
    'North Field',
    'Pleasant Grove',
    'Pleasant Grove East',
    'Pleasant Grove West',
    'Timpanogos'
]

numfiles = len(sys.argv)
if (numfiles > 0):
    compare_file = sys.argv[1]
    if compare_file in stake_list:
        stake = compare_file 
    else:
        stake = 'all'
else:
    stake = ''

logging.basicConfig(filename='data/results/Update {0}-{1}.txt'.format(compare_file, str(datetime.today()).split()[0]), level=logging.DEBUG)
log1 = logging.getLogger('Update')
logging.debug('\n*** {0} ***'.format(compare_file))

# Load in saved database and convert to JSON fuzzy format for comparison
counselors = handle_csv.load_counselors('data/MBC_db.csv', stake)
fuzzy_comparable_counselors = handle_csv.make_fuzzy_comparable_counselor_list(counselors)
fuzzy_results = []

"""Load in one data file and convert to JSON fuzzy format for comparison.
   Find matching entries for each MB Counselor in the database, and return 
   with information. Write to the log all info that needs to be updated online.
"""
if (compare_file == 'MBC'):
    new_counselors = handle_csv.load_counselors('data/MBC.csv', stake)
    new_fuzzy_comparable_counselors = handle_csv.make_fuzzy_comparable_counselor_list(new_counselors)
    for c in fuzzy_comparable_counselors:
        fuzzy_results.append(compare.find_match(c, new_fuzzy_comparable_counselors))

elif (compare_file == 'YPT'):
    dist_scouters = handle_csv.load_dist_ypt('data/YPT.csv')
    fuzzy_comparable_scouters = handle_csv.make_fuzzy_comparable_district_list(dist_scouters)
    for c in fuzzy_comparable_counselors:
        fuzzy_results.append(compare.find_match(c, fuzzy_comparable_scouters))

elif len(stake):
    all_households = handle_json.read_in_stake('data/{0}.json'.format(stake))
    fuzzy_comparable_members = handle_json.make_fuzzy_comparable_member_list(all_households)
    for c in fuzzy_comparable_counselors:
        fuzzy_results.append(compare.fuzzy_compare(c, fuzzy_comparable_members))

else:
    logging.info('No stake selected for matching')

if len(fuzzy_results):
    for c in fuzzy_results:
        counselor = c['counselor']
        match     = c['match']

        if (c['match_type'] == 'moved   '):
            logging.info('\n{0} : {1}, {2} \t{3}'.format(c['match_type'], counselor['last_name'], counselor['first_name'], counselor['street']))
            logging.info('new owner: {0}, {1} {2}\n'.format(match['last_name'], match['first_name'], match['street']))

        elif (c['match_type'] == 'unknown ' or c['match_type'] == 'possible'):
            logging.info('\n{0}'.format(c['match_type']))
            logging.info('{0}, {1}\t{2} {3} {4}'.format(counselor['last_name'], counselor['first_name'], counselor['street'], counselor['phones'], counselor['emails']))
            # logging.info('{0}, {1}\t{2} {3} {4}'.format(    match['last_name'],     match['first_name'],     match['street'],     match['phones'],     match['emails']))

        else:
            logging.info('\n{0} : {1} {2} ({3}) : {4}'.format(c['match_type'], counselor['last_name'], counselor['first_name'], match['first_name'] if (c['match_type'] == 'probable')else '',match['full_name']))
            logging.info('Addresses: {0} <--> {1}'.format(counselor['street'], match['street']))
            logging.info('Ward: {0}'.format(match['ward']))
            if  (compare_file == 'YPT'):
                logging.info(match)
                
            if       match['phones']['phone1']:
                if ((match['phones']['phone1'] != counselor['phones']['phone1']) and
                    (match['phones']['phone1'] != counselor['phones']['phone2'])):
                    logging.info('New Phone* {0} (was {1})'.format(match['phones']['phone1'],counselor['phones']['phone1']))
            if       match['phones']['phone2']:
                if ((match['phones']['phone2'] != counselor['phones']['phone1']) and
                    (match['phones']['phone2'] != counselor['phones']['phone2'])):
                    logging.info('New Phone* {0} (was {1})'.format(match['phones']['phone2'],counselor['phones']['phone2']))
            if   len(match['emails']['email1']):
                if ((match['emails']['email1'] != counselor['emails']['email1']) and
                    (match['emails']['email1'] != counselor['emails']['email2'])):
                    logging.info('New eMail* {0} (was {1})'.format(match['emails']['email1'],counselor['emails']['email1']))
            if   len(match['emails']['email2']):
                if ((match['emails']['email2'] != counselor['emails']['email1']) and
                    (match['emails']['email2'] != counselor['emails']['email2'])):
                    logging.info('New eMail* {0} (was {1})'.format(match['emails']['email2'],counselor['emails']['email2']))



# get exact matches
exact_matches    = [x for x in fuzzy_results if (x['match_type'] == 'matched ')]
# get widened matches
probable_matches = [x for x in fuzzy_results if (x['match_type'] == 'probable')]
# get mismatches
possible_matches = [x for x in fuzzy_results if (x['match_type'] == 'possible')]
# get no matches
not_matches      = [x for x in fuzzy_results if (x['match_type'] == 'moved   ')]
unknown_matches  = [x for x in fuzzy_results if (x['match_type'] == 'unknown ')]

print '\n *****  RESULTS  *****\n'


print '\n'
print 'exact matches: {0}'        .format(len(exact_matches))
print 'probable matches: {0}'     .format(len(probable_matches))
print 'possible matches: {0}'     .format(len(possible_matches))
print 'total matches: {0}'        .format(len(exact_matches) + len(probable_matches) + len(possible_matches))
print 'move outs: {0}'            .format(len(not_matches))
print 'total unknown: {0}'        .format(len(unknown_matches))
print 'total searched: {0}'       .format(len(fuzzy_comparable_counselors))
print 'find percentage: {0}'.format(float(len(exact_matches) + len(probable_matches) + len(possible_matches))/(float(len(fuzzy_comparable_counselors))))

with open('matches-{0}.json'.format(stake), 'wb') as f:
    f.write(json.dumps(fuzzy_results))

print 'File write complete'