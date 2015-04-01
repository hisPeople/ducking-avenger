import string


def normalize_phone_number(phone):
    """Remove any non digits from phone and return string"""
    if phone:
        # convert unicode to ascii because python sux
        phone = phone.encode('utf8')
        trans = string.maketrans('', '')
        digit_trans = trans.translate(trans, string.digits)
        phone = phone.translate(trans, digit_trans)

        # convert it back to unicode because python sux
        phone = phone.encode('ascii')
    return phone

stake_dict = {
    '03-1': 'Community Units',
    '03-3': 'Timpanogos',
    '03-4': 'North Field',
    '03-5': 'Garden',
    '03-6': 'Lindon Central',
    '03-7': 'Mount Mahogany',
    '03-8': 'Lindon',
    '03-9': 'Lindon West',
    '03-A': 'Pleasant Grove East',
    '03-B': 'Grove Creek',
    '03-C': 'Pleasant Grove',
    '03-D': 'Pleasant Grove West'
}

def stake_ID(stake_code):
    """Remove any non digits from phone and return string"""
    if stake_code in stake_dict:
        return stake_dict[stake_code]
    else:
        return ''