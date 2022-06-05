def unescape(word):
    if word.endswith('\r\n'):
        word = word.replace('\r\n', '')
    if word.startswith('"'):
        word = word[1:-1]
    word = word.replace('""', '"')
    return word


def escape(word):
    word = str(word)
    word = word.replace('"', '""')
    if ',' in word or '"' in word:
        word = f'"{word}"'
    return word
