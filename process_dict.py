__author__ = 'devonmoss'

from fuzzywuzzy import process


def extract_best_dict(query, choices, compare_rules):
    """Find the dictionary from choices that best matches the query dictionary
    based on the rules in comparison and return it.

    Args:
        query (dict) -- Query info::

        {
            last_name: 'smith',
            first_name: 'jonathan',
            street: '1234 Meadow Ln',
            email: 'johnsmith@gmail.com',
            phone: '123-456-7890'
        }

        choices (list) -- Search against::

        [
            {
                last_name: 'Anderson',
                first_name: 'Tom',
                street: '3932 E 30 S',
                email: 'tander@hotmail.com',
                phone: '343-434-2343'
            },
            {
                last_name: 'Smith',
                first_name: 'Jonathan',
                street: '1234 Meadow Ln',
                email: 'johnsmith@gmail.com',
                phone: '123-456-7890'
            }
        ]

        compare_rules (CompareRules) -- rules for finding best match

    Returns:
        dict. Closest match to query found in choices
    """

    best_match_total = 0

    for k in query.keys():
        best_key_match = 0
