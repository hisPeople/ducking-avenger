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