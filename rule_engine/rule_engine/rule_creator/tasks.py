import validators


def valid_url(url):
    valid = False
    try:
        if validators.url(url):
            valid = True
    except Exception as exception:
        valid = False
        raise Exception("Exception occurred while checking url validity : %s" % exception)
    finally:
        return valid