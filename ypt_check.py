import cProfile

__author__ = 'devonmoss'

import requests
import csv
import json
import handle_csv
import compare



dist_scouters = handle_csv.get_dist_ypt('data/Timp Dist YPT.csv')
fuzzy_comparable_members = handle_csv.make_fuzzy_comparable_district_list(dist_scouters)

counselors = handle_csv.get_counselors_in_stake('data/CounselorList141108.csv', 'Pleasant Grove East')
fuzzy_comparable_counselors = handle_csv.make_fuzzy_comparable_counselor_list(counselors)

fuzzy_results = []
for c in fuzzy_comparable_counselors:
    # total_matches = total_matches + compare.fuzzy_compare(c, fuzzy_comparable_members)
    fuzzy_results.append(compare.fuzzy_compare(c, fuzzy_comparable_members))


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

for c in fuzzy_results:
    counselor = c['counselor']
    print 'counselor: \t {0} {1} {2}'.format(counselor['first_name'], counselor['last_name'], counselor['street'])
    # print '{0}' .format(c['match_type'])
    if (c['match_type'] == 'moved   '):
        new_owner = c['match']
        print '{0}\t   * new owner: {1}\n'.format(c['match_type'], new_owner['last_name'])
    elif (c['match_type'] == 'unknown '):
        print 'Unknown\n'
    else:
        match = c['match']
        print '{0}\t {1} {2} {3}\n'.format(c['match_type'], match['first_name'], match['last_name'], match['street'])


print '\n'
print 'exact matches: {0}'        .format(len(exact_matches))
print 'probable matches: {0}'     .format(len(probable_matches))
print 'possible matches: {0}'     .format(len(possible_matches))
print 'total matches: {0}'        .format(len(exact_matches) + len(probable_matches) + len(possible_matches))
print 'move outs: {0}'            .format(len(not_matches))
print 'total unknown: {0}'        .format(len(unknown_matches))
print 'total searched: {0}'       .format(len(fuzzy_comparable_counselors))
print 'find percentage: {0}'.format(float(len(exact_matches) + len(probable_matches) + len(possible_matches))/(float(len(fuzzy_comparable_counselors))))

