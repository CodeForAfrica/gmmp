from ._recodes import recode


def canon(key):
    if key:
        canon_key = key.replace("…", "")
        canon_key = recode(canon_key.strip())
        return canon_key.strip().lower()
    return ""
