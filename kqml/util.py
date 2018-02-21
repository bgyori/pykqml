def safe_decode(txt):
    """Return decoded text if it's not already bytes."""
    try:
        return txt.decode()
    except AttributeError:
        return txt


def safe_encode(txt):
    """Return encoded text if it's not already str."""
    try:
        return txt.encode()
    except AttributeError:
        return txt
