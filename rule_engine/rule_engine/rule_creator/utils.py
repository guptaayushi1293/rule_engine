import validators


def valid_url(url):
    valid = False
    try:
        if validators.url(url):
            valid = True
    except Exception as exception:
        print("Exception : %s" % exception)
        valid = False
    finally:
        return valid
