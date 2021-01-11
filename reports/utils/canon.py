from reports.utils.recodes import recode


def canon(key):
    if key:
        key = key.replace(u'\u2026', '')
        key = recode(key.strip())
        return key.strip().lower()
    return ''
