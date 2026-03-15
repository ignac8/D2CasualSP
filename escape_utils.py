def unescape(word):
    word = word.rstrip('\r\n')
    if word.startswith('"'):        # quoted field — strip wrapping quotes
        word = word[1:-1]
    word = word.replace('""', '"')  # doubled quotes → literal quote
    return word


def escape(word):
    word = str(word)
    needs_quoting = ',' in word or '"' in word
    word = word.replace('"', '""')  # literal quote → doubled quotes
    if needs_quoting:               # wrap field if it contains , or "
        word = f'"{word}"'
    return word
